import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime
import re

def process_mamee_invoice_file(dataframe):
    invoice = {'new_item': [], 'sales_invoice':[]}
    dataframe = pd.read_excel(dataframe, header=3)  
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Customer Code','Customer Name','Transaction Type','Transaction No.','Product Code','Transaction Date','Salesman','Product Hierarchy Level 4','Conversion Unit','Unit Price (MYR)','Net Price(MYR)','Discount Amt (MYR)','Qty','UOM','Selling Type']]

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
            net_amount = row['Net Price(MYR)']
            discount_amount = row['Discount Amt (MYR)']
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
                    'invoice_date': int(invoice_date),
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
    dataframe = pd.read_excel(dataframe, header=3)
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
            net_amount = row['Net Price(MYR)']
            discount_amount = row['Discount Amt (MYR)']
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
                    'cn_date': str(int(cn_date)),
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