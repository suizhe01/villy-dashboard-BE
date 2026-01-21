from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
import math
from datetime import datetime

def get_kara_item_itemuom(file):
    try:
        new_item = []
        dataframe = pd.read_excel(file, header=2,sheet_name=1)
        item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}
        store_itemcode = []

        with pd.option_context('display.max_row', None):
            selected_columns = dataframe[['ItemCode','Description','UOM','Rate','Price','UOM.1','Rate.1','Price.1']]

            for index, row in selected_columns.iterrows():
                item_code= row['ItemCode']
                description = row['Description']
                uom = row['UOM']
                rate = row['Rate']
                price = row['Price']
                unit_uom = row['UOM.1']
                unit_rate = row['Rate.1']
                unit_price = row['Price.1']
                
                # unit_uom = 'UNT' if unit_uom == 'unit' else unit_uom
                item_key = (str(item_code),uom)
                if item_key not in store_itemcode and item_key not in item_uom_dict:
                    store_itemcode.append(item_key)
                    new_item.append({
                        'item_code': int(item_code),
                        'description': description,
                        'uom': uom,
                        'rate':rate,
                        'price':price,
                        'unit_uom': unit_uom,
                        'unit_rate':unit_rate,
                        'unit_price':unit_price,
                        'trigger_file_type': 'AddItem'
                    })

        return JsonResponse(new_item,safe=False, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def process_kara_invoice_file(uploaded_file):
    sales = {'new_item':[],'sales_invoice':[]}
    dataframe = pd.read_excel(uploaded_file, header=14)  
    store_itemcode = []

    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}


    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Cust Ref', 'Cust Name', 'Doc No','Doc Date','Prd Code','Prd Description','Unit Price (RM)','Qty','UOM', 'Promo Disc Amt (RM)','Net Amt (RM)','Route Code','Gross Amt (RM)']]

        for index, row in selected_columns.iterrows():
            debtor_code = row['Cust Ref']
            debtor_name = row['Cust Name']
            transaction_no = row['Doc No']
            transaction_date = row['Doc Date']
            item_code = row['Prd Code']
            description = row['Prd Description']
            quantity = row['Qty']
            uom = row['UOM']
            price = row['Unit Price (RM)']
            # rate = row['conversion_unit']
            # total_price = row['total_price'] # is qualt to total_amount header
            sales_agent = row['Route Code']
            discount_amt = row['Promo Disc Amt (RM)']
            net_amount = row['Net Amt (RM)']
            gross_amount = row['Gross Amt (RM)']

            
            if math.isnan(discount_amt):
                discount_amt = float(0)

            rate = 0
            
            piece_price = 0
            item_key = (str(item_code), uom)

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append((item_code,uom))
                if uom == 'CTN':
                    sales['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': uom,
                        'price': price,
                        'rate': rate,
                        'unit_uom': 'UNT',
                        'unit_price': piece_price,
                        'unit_rate': 1,
                        'trigger_file_type': 'AddItem'
                    })
                elif uom == 'UNT':
                    sales['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': uom,
                        'price': price,
                        'rate': rate,
                        'unit_uom': uom,
                        'unit_price': piece_price,
                        'unit_rate': 1,
                        'trigger_file_type': 'AddItem'
                    })
                else:
                    return JsonResponse('error', safe=False, status=status.HTTP_404_NOT_FOUND)

            if uom == 'CTN':
                price = gross_amount/quantity

            sales['sales_invoice'].append({
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'invoice_no': transaction_no,
                    'invoice_date': transaction_date,
                    'description': description,
                    'item_code': item_code,
                    'quantity': quantity,
                    'rate': rate,
                    'uom': uom,
                    'sales_agent': sales_agent,
                    'discount_amt': discount_amt,
                    'net_amt': net_amount,
                    'price': price
            })

    return JsonResponse(sales, safe=False, status=status.HTTP_200_OK)

def process_kara_cn_file(uploaded_file):
    cn = {'new_item':[],'cn':[]}
    dataframe = pd.read_excel(uploaded_file, header=15)  
    store_itemcode = []

    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}


    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Route Code','Cust Ref','Cust Name','CN No','Txn Date','Product Code','Product Description','Qty in Unit','Gross Amount (RM)','Reason','Promo Discount (RM)','Net Amount (RM)', 'Remark']]

        current_cn_no = None
        seq = 0

        for index, row in selected_columns.iterrows():
            cn_no = row['CN No']
            cn_date = datetime.strptime(row['Txn Date'], '%d/%m/%Y').strftime('%Y-%m-%d')
            customer_code = row['Cust Ref']
            customer_name = row['Cust Name']
            sales_agent = row['Route Code']
            item_code = row['Product Code']
            description = row['Product Description']
            uom = 'UNT'
            quantity = row['Qty in Unit']
            price = row['Gross Amount (RM)']
            discount_amount = row['Promo Discount (RM)']
            net_amount = row['Net Amount (RM)']
            reason = row['Reason']
            seq = index + 1 
            our_invoice = row['Remark']

            if pd.isna(our_invoice):
                our_invoice = ''

            if cn_no != current_cn_no:
                current_cn_no = cn_no
                seq = 1
            else:
                seq += 1

            item_key =  (str(item_code), uom)
            
            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)

                unit_price = price/quantity

                cn['new_item'].append({
                    'item_code': item_code,
                    'description': description,
                    'uom': 'CTN',
                    'rate': 0,
                    'price': 0,
                    'unit_uom': 'UNT',
                    'unit_price': unit_price,
                    'unit_rate': 1,
                    'trigger_file_type': 'AddItem'
                }) 

            # cn_date_formatted = cn_date.strftime('%Y-%m-%d')

            if uom == 'UNT':
                price = price/quantity

            cn['cn'].append({
                'cn_no': cn_no,
                'cn_date': cn_date,
                'customer_name': customer_name,
                'customer_code': customer_code,
                'seq': seq,
                'sales_agent': sales_agent,
                'item_code': item_code,
                'description': description,
                'quantity': abs(quantity),
                'uom': uom,
                'discount_amount': abs(discount_amount),
                'net_amount': abs(net_amount),
                'price': price,
                'reason': reason,
                'our_invoice': our_invoice
            })

    return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)