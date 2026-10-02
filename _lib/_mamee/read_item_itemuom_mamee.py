import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime
import re

# The DMS report has come in two layouts: the older one has its column names on
# row 4 with "(MYR)" price headers and dates as numbers (20260929); the newer
# one has filter rows above, column names on row 10, shorter price headers and
# real dates. Both are read the same way below.
NEW_COLUMN_NAMES = {
    'Material Group': 'Product Hierarchy Level 4',
    'Unit Price': 'Unit Price (MYR)',
    'Net Price': 'Net Price(MYR)',
    'Discount Amt': 'Discount Amt (MYR)',
}

def read_mamee_sheet(file):
    """Read the report from its column-name row, using the older column names.

    Stops at the last line that has a Transaction Type, so a "Page 1 of 1"
    footer is not read: it would turn whole-number columns such as Qty and
    Conversion Unit into decimals or text.
    """
    sheet = pd.read_excel(file, header=None)
    header_row, last_row = 3, None
    for index, row in sheet.iterrows():
        names = [str(value).strip() for value in row]
        if 'Customer Code' in names:
            header_row = index
            if 'Transaction Type' in names:
                last_row = sheet.iloc[header_row + 1:, names.index('Transaction Type')].last_valid_index()
            break
    if hasattr(file, 'seek'):
        file.seek(0)
    dataframe = pd.read_excel(file, header=header_row,
                              nrows=None if last_row is None else last_row - header_row)
    return dataframe.rename(columns={new: old for new, old in NEW_COLUMN_NAMES.items()
                                     if new in dataframe.columns and old not in dataframe.columns})

def date_number(value):
    """20260929 for either a number date or a real date."""
    if isinstance(value, (datetime, pd.Timestamp)):
        return int(value.strftime('%Y%m%d'))
    return int(value)

def zero_if_blank(value):
    return 0.0 if pd.isna(value) else value

def process_mamee_invoice_file(dataframe):
    invoice = {'new_item': [], 'sales_invoice':[]}
    dataframe = read_mamee_sheet(dataframe)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Customer Code','Customer Name','Transaction Type','Transaction No.','Product Code','Transaction Date','Salesman','Product Hierarchy Level 4','Conversion Unit','Unit Price (MYR)','Net Price(MYR)','Discount Amt (MYR)','Qty','UOM']]

        for index, row in selected_columns.iterrows():
            debtor_code = row['Customer Code']
            debtor_name = row['Customer Name']
            transaction_type = row['Transaction Type']
            invoice_no = row['Transaction No.']
            invoice_date = row['Transaction Date']
            item_code = row['Product Code']
            salesman = row['Salesman']
            description = row['Product Hierarchy Level 4']
            rate = row['Conversion Unit']
            carton_price = row['Unit Price (MYR)']
            uom = row['UOM']
            net_amount = zero_if_blank(row['Net Price(MYR)'])
            discount_amount = zero_if_blank(row['Discount Amt (MYR)'])
            quantity = row['Qty']

            item_key = (str(item_code), uom)
            price = carton_price if uom == 'CTN' else 0
            unit_price = 0

            if transaction_type == 'Invoice':
                if item_key not in item_uom_dict and item_key not in store_itemcode:
                    store_itemcode.append(item_key)
                    unit_uom = 'PCK'

                    if ')P' in description or 'Cup' in description:
                        unit_uom = 'CUP'

                    if uom == 'PCK':
                        rate = 1
                        unit_uom = 'PCK'
                    elif uom == 'CUP':
                        rate = 1
                        unit_uom = 'CUP'
                    elif uom == 'CAN':
                        rate = 1
                        unit_uom = 'CAN'

                    if '+' in description:
                        match = re.search(r'\d+[+]\d+', description)
                        if match:
                            extracted = match.group()
                            num1, num2 = map(int, re.split('[+]', extracted))

                            unit_price = round(carton_price/rate/(num1+num2),2)

                            if uom == 'CTN':
                                pass
                            elif uom == 'BDL':
                                price = carton_price/rate
                            else:
                                price = round(carton_price/rate/(num1+num2),2)
                                # if '(P)' in description:
                                #     unit_price = round(carton_price/rate/rate,2)
                                # else:
                                #     unit_price = round(carton_price/rate/num1,2)

                        else:
                            print("Pattern not found:", description)
                    else:
                        match = re.search(r'\d+[xX]\d+', description)
                        if match:
                            extracted = match.group()
                            num1, num2 = map(int, re.split('[xX]', extracted))
                            if uom == 'CTN':
                                pass
                            elif uom == 'BDL':
                                price = carton_price/rate
                            else:
                                price = round(carton_price/num1/num2,2)

                            unit_price = round(carton_price/num1/num2,2)
                        else:
                            print("Pattern not found:", description)

                    invoice['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': uom,
                        'price': price,
                        'rate': rate,
                        'unit_uom': unit_uom,
                        'unit_price': unit_price,
                        'unit_rate': 1,
                        'carton_price': carton_price,
                        'trigger_file_type': 'Invoice'
                    })
            
            
                if ',' in str(net_amount):
                    net_amount = float(net_amount.replace(',',''))
                # print(discount_amount)
                invoice['sales_invoice'].append({
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'invoice_no': invoice_no,
                    'invoice_date': date_number(invoice_date),
                    'salesman': salesman,
                    'net_amount': float(net_amount),
                    'discount_amount': float(discount_amount) if isinstance(discount_amount, (int, float)) else float(str(discount_amount).replace(',', '')),
                    'quantity': quantity,
                    'item_code':item_code,
                    'description': description,
                    'price': float(net_amount)/quantity,
                    'uom': uom,
                    'rate': rate,
                })

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)

def process_mamee_cn_file(dataframe):
    dataframe = read_mamee_sheet(dataframe)
    dataframe = dataframe.dropna(how='all')

    cn = {'new_item': [], 'cn': []} 
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Customer Code','Customer Name','Transaction Type','Transaction No.','Product Code','Transaction Date','Salesman','Product Hierarchy Level 4','Conversion Unit','Unit Price (MYR)','Net Price(MYR)','Discount Amt (MYR)','Qty','UOM']]
        for index, row in selected_columns.iterrows():
            if row.isna().all():
                # Skip this row if all elements are NaN
                continue
            debtor_code = row['Customer Code']
            debtor_name = row['Customer Name']
            transaction_type = row['Transaction Type']
            cn_no = row['Transaction No.']
            cn_date = row['Transaction Date']
            salesman = row['Salesman']
            item_code = row['Product Code']
            description = row['Product Hierarchy Level 4']
            rate = row['Conversion Unit']
            carton_price = row['Unit Price (MYR)']
            net_amount = zero_if_blank(row['Net Price(MYR)'])
            discount_amount = zero_if_blank(row['Discount Amt (MYR)'])
            quantity = row['Qty']
            uom = row['UOM']

            price = carton_price if uom == 'CTN' else 0
            item_key = (str(item_code), uom)
            unit_price = 0

            if transaction_type == 'Credit Note':
                if item_key not in item_uom_dict and item_key not in store_itemcode:
                    store_itemcode.append(item_key)
                    unit_uom = 'PCK'

                    if ')P' in description or 'Cup' in description:
                        unit_uom = 'CUP'

                    if uom == 'PCK':
                        rate = 1
                        unit_uom = 'PCK'
                    elif uom == 'CUP':
                        rate = 1
                        unit_uom = 'CUP'
                    elif uom == 'CAN':
                        rate = 1
                        unit_uom = 'CAN'

                    if '+' in description:
                        match = re.search(r'\d+[+]\d+', description)
                        if match:
                            extracted = match.group()
                            num1, num2 = map(int, re.split('[+]', extracted))

                            unit_price = round(carton_price/rate/(num1+num2),2)

                            if uom == 'CTN':
                                pass
                            elif uom == 'BDL':
                                price = carton_price/rate
                            else:
                                price = round(carton_price/rate/(num1+num2),2)
                                # if '(P)' in description:
                                #     unit_price = round(carton_price/rate/rate,2)
                                # else:
                                #     unit_price = round(carton_price/rate/num1,2)

                        else:
                            print("Pattern not found:", description)
                    else:
                        match = re.search(r'\d+[xX]\d+', description)
                        if match:
                            extracted = match.group()
                            num1, num2 = map(int, re.split('[xX]', extracted))
                            if uom == 'CTN':
                                pass
                            elif uom == 'BDL':
                                price = carton_price/rate
                            else:
                                # print('hello', carton_price, item_code)
                                price = round(carton_price/num1/num2,2)

                            unit_price = round(carton_price/num1/num2,2)
                        else:
                            print("Pattern not found:", description)
                
                    cn['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': uom,
                        'price': price,
                        'rate': int(rate),
                        'unit_uom': unit_uom,
                        'unit_price': abs(unit_price),
                        'unit_rate': 1,
                        'carton_price': carton_price,
                        'trigger_file_type': 'CN'
                    })

                if ',' in str(net_amount):
                    net_amount = float(net_amount.replace(',',''))
                

                cn['cn'].append({
                    'cn_no': cn_no,
                    'cn_date': str(date_number(cn_date)),
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'item_code': item_code,
                    'description': description,
                    'uom':uom,
                    'quantity': int(abs(quantity)),
                    'discount_amount': abs(discount_amount),
                    'net_amount': abs(float(net_amount)),
                    'sales_agent': salesman
                })

    return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)