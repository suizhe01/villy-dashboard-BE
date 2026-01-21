import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime

def process_mamee_purchase_file(dataframe):
    purchase = {'new_item':[], 'purchase_invoice': []}
    dataframe = pd.read_excel(dataframe, header=6)  
    for col in dataframe.columns:
        if col.startswith('Unnamed'):
            dataframe.rename(columns={col: 'Description'}, inplace=True)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.all() if item.uom == 'CTN'}
    print(item_uom_dict)
    with pd.option_context('display.max_row', None):
        selected_dksh_column = dataframe[['Txn Date','Stock Receipt No', 'Product','Description','Received','Entered(MYR)','Value(MYR)','DO No']]
        
        for index, row in selected_dksh_column.iterrows():
            invoice_date = row['Txn Date']
            stock_received_no = row['Stock Receipt No']
            item_code = row['Product']
            description = row['Description'][2]
            # print(description)
            quantity = str(row['Received'])
            price = row['Entered(MYR)']
            net_price = row['Value(MYR)']
            do_no = row['DO No']

            # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom='CTN')
            item_key = (item_code, 'CTN')
            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                # print('ok?')
                purchase['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': 'CTN',
                        'price': price,
                        'rate': 0,
                        'bundle_uom': 'BDL',
                        'bundle_price': 0,
                        'bundle_rate': 0,
                        'unit_uom': 'UNT',
                        'unit_price': 0,
                        'unit_rate': 1,
                        'trigger_file_type': 'Purchase'
                })

            purchase['purchase_invoice'].append({
                'purchase_invoice_no' : stock_received_no,
                'delivery_no': do_no,
                'item_code': item_code,
                'transaction_date': invoice_date,
                'quantity': quantity,
                'net_price' : net_price,
            })

    return JsonResponse(purchase, safe=False, status=status.HTTP_200_OK)

# def process_mamee_invoice_file(dataframe):
#     invoice = {'new_item': [], 'invoice':[]}
#     dataframe = pd.read_excel(dataframe, header=3)  
#     store_itemcode = []
#     item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.all()}

#     with pd.option_context('display.max_row', None):
#         selected_columns = dataframe[['Customer Code','Customer Name','Transaction Type','Transaction No.','Product Code','Transaction Date','Salesman','Product Hierarchy Level 4','Conversion Unit','Unit Price (MYR)','Net Price(MYR)','Discount Amt (MYR)','Qty','UOM','Selling Type']]

#         for index, row in selected_columns.iterrows():
#             debtor_code = row['Customer Code']
#             debtor_name = row['Customer Name']
#             transaction_type = row['Transaction Type']
#             invoice_no = row['Transaction No.']
#             invoice_date = row['Transaction Date']
#             item_code = row['Product Code']
#             salesman = row['Salesman']
#             description = row['Product Hierarchy Level 4']
#             rate = row['Conversion Unit']
#             carton_price = row['Unit Price (MYR)']
#             uom = row['UOM']
#             net_amount = row['Net Price(MYR)']
#             discount_amount = row['Discount Amt (MYR)']
#             quantity = row['Qty']
#             selling_type = row['Selling Type']
            
#             if transaction_type == 'Invoice' and selling_type == 'S':
#                 item_key = (item_code, uom)
#                 # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom=uom)
#                 price = carton_price if uom == 'CTN' else 0
#                 if item_key not in item_uom_dict and item_key not in store_itemcode:
#                     store_itemcode.append(item_key)
#                     invoice['new_item'].append({
#                         'item_code': item_code,
#                         'description': description,
#                         'uom': uom,
#                         'price': price,
#                         'rate': rate,
#                         'unit_uom': 'UNT',
#                         'unit_price': 0,
#                         'unit_rate': 1,
#                         'carton_price': carton_price,
#                         'trigger_file_type': 'Invoice'
#                     })
                
#                 invoice['invoice'].append({
#                     'debtor_code': debtor_code,
#                     'debtor_name': debtor_name,
#                     'invoice_no': invoice_no,
#                     'invoice_date': invoice_date,
#                     'salesman': salesman,
#                     'net_amount': net_amount,
#                     'discount_amount': discount_amount,
#                     'quantity': quantity,
#                     'item_code':item_code,
#                     'uom': uom
#                 })

#     return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)

# def process_mamee_cn_file(dataframe):
#     dataframe = pd.read_csv(dataframe, header=3)
#     dataframe = dataframe.dropna(how='all')

#     cn = {'new_item': [], 'cn': []} 
#     store_itemcode = []
#     item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.all()}

#     with pd.option_context('display.max_row', None):
#         selected_columns = dataframe[['Customer Code','Customer Name','Transaction Type','Transaction No.','Product Code','Transaction Date','Salesman','Product Hierarchy Level 4','Conversion Unit','Unit Price (MYR)','Net Price(MYR)','Discount Amt (MYR)','Qty','UOM']]
#         for index, row in selected_columns.iterrows():
#             if row.isna().all():
#                 # Skip this row if all elements are NaN
#                 continue
#             debtor_code = row['Customer Code']
#             debtor_name = row['Customer Name']
#             transaction_type = row['Transaction Type']
#             cn_no = row['Transaction No.']
#             cn_date = row['Transaction Date']
#             salesman = row['Salesman']
#             item_code = row['Product Code']
#             description = row['Product Hierarchy Level 4']
#             rate = row['Conversion Unit']
#             carton_price = row['Unit Price (MYR)']
#             net_amount = row['Net Price(MYR)']
#             discount_amount = row['Discount Amt (MYR)']
#             quantity = row['Qty']
#             uom = row['UOM']

#             item_key = (item_code, uom)
#             if transaction_type == 'Credit Note':
#                 price = carton_price if uom == 'CTN' else 0
#                 uom = 'UNT' if uom == 'PCK' else uom
#                 rate = rate if uom == 'CTN' else 0
#                 if item_key not in item_uom_dict and item_key not in store_itemcode:
#                     store_itemcode.append(item_key)
#                     cn['new_item'].append({
#                         'item_code': item_code,
#                         'description': description,
#                         'uom': uom,
#                         'price': price,
#                         'rate': int(rate),
#                         'unit_uom': 'UNT',
#                         'unit_price': 0,
#                         'unit_rate': 1,
#                         'carton_price': carton_price,
#                         'trigger_file_type': 'CN'
#                     })
                
#                 if ',' in net_amount:
#                     net_amount = float(net_amount.replace(',',''))
                
#                 if discount_amount >0.0:
#                     cn['cn'].append({
#                         'cn_no': cn_no,
#                         'cn_date': str(int(cn_date)),
#                         'debtor_code': debtor_code,
#                         'debtor_name': debtor_name,
#                         'item_code': item_code,
#                         'uom':uom,
#                         'quantity': int(abs(quantity)),
#                         'discount_amount': abs(discount_amount),
#                         'net_amount': abs(net_amount),
#                         'sales_agent': salesman
#                     })
#                 else:
#                     cn['cn'].append({
#                         'cn_no': cn_no,
#                         'cn_date': str(int(cn_date)),
#                         'debtor_code': debtor_code,
#                         'debtor_name': debtor_name,
#                         'item_code': item_code,
#                         'uom':uom,
#                         'quantity': int(abs(quantity)),
#                         'discount_amount': abs(discount_amount),
#                         'net_amount': abs(float(net_amount)),
#                         'sales_agent': salesman
#                     })

#     return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)