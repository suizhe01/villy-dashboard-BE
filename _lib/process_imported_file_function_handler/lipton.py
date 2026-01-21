import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from item.models import Item

def process_lipton_purchase_file(dataframe):
    dataframe = pd.read_csv(dataframe)
    purchase = {'new_item':[], 'purchase_invoice':[]}
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.all()}

    with pd.option_context('display.max_row', None):
        selected_lipton_columns = dataframe[['Prd Code', 'Prd Description', 'UOM', 'Unit Price','Doc No','Doc Type','Doc Date', 'Expiry Date','Invoice Qty','Received Qty','Net Amt']]
        
        for index, row in selected_lipton_columns.iterrows():
            item_code = row['Prd Code']
            description = row['Prd Description']
            uom = row['UOM']
            case_price = row['Unit Price']
            invoice_no = row['Doc No']
            invoice_date = row['Doc Date']
            product_expiry_date = row['Expiry Date']
            quantity = row['Received Qty']
            net_amount = row['Net Amt']
            doc_type = row['Doc Type']
            
            
            if doc_type == 'Company Inv':
                # is_item_exist = ItemUOM.objects.filter(uom=uom,itemcode=item_code)
                item_key = (item_code, uom)
                if item_key not in item_uom_dict and item_key not in store_itemcode:
                    store_itemcode.append(item_key)
                    price = case_price if uom == 'Case' else 0
                    purchase['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': uom,
                        'price': price,
                        'rate': 0,
                        'unit_uom': 'UNT',
                        'unit_price': 0,
                        'unit_rate': 1,
                        'case_price': case_price,
                        'trigger_file_type': 'Purchase'
                })
                
                purchase['purchase_invoice'].append({
                    'purchase_invoice_no': invoice_no,
                    'purchase_invoice_date': invoice_date,
                    'item_code': item_code,
                    'quantity': quantity,
                    'product_expiry_date': product_expiry_date,
                    'net_amount': net_amount,
                    'uom': uom
                })

    return JsonResponse(purchase, safe=False, status=status.HTTP_200_OK)

# def process_lipton_invoice_file(uploaded_file):
#     dataframe = pd.read_csv(uploaded_file)
#     invoice = {'new_item': [], 'invoice':[]}
#     store_itemcode = []
#     item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.all()}
#     # print(datetime.now())
#     with pd.option_context('display.max_row', None):
#         selected_columns = dataframe[['Cust Code','Cust Name','Doc No','Doc Date','Doc Type','Status','Prd Code','Prd Description','Qty','UOM','Default UOM Price','Net Amt','Promo Disc Amt']]

#         for index, row in selected_columns.iterrows():
#             debtor_code = row['Cust Code']
#             debtor_name = row['Cust Name']
#             invoice_no = row['Doc No']
#             invoice_date = row['Doc Date']
#             doc_type = row['Doc Type']
#             doc_status = row['Status']
#             item_code = row['Prd Code']
#             description = row['Prd Description']
#             quantity = row['Qty']
#             uom = row['UOM']
#             carton_price = row['Default UOM Price']
#             net_amount = row['Net Amt']
#             discount_amount = row['Promo Disc Amt']

#             if doc_type == 'Inv' and doc_status == 'Confirmed':
#                 uom = 'UNT' if uom == 'PC' else 'CTN' if uom == 'CS' else uom
#                 price = carton_price if uom == 'CTN' else 0
#                 item_key = (item_code, uom)
#                 # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom=uom)
#                 if item_key not in item_uom_dict and item_key not in store_itemcode:
#                     store_itemcode.append(item_key)
#                     invoice['new_item'].append({
#                         'item_code': item_code,
#                         'description': description,
#                         'uom': uom,
#                         'price': price,
#                         'rate': 0,
#                         'unit_uom': 'UNT',
#                         'unit_price': 0,
#                         'unit_rate': 1,
#                         'carton_price': carton_price,
#                         'trigger_file_type': 'Invoice'
#                 })
                    
#                 invoice['invoice'].append({
#                     'debtor_code': debtor_code,
#                     'debtor_name':debtor_name,
#                     'invoice_no': invoice_no,
#                     'invoice_date': invoice_date,
#                     'net_amount':net_amount,
#                     'discount_amount': discount_amount,
#                     'quantity': quantity,
#                     'item_code': item_code,
#                     'uom': uom
#                 })
#     # print(datetime.now())

#     return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)

# def process_lipton_cn_file(uploaded_file):
#     dataframe = pd.read_csv(uploaded_file)
#     cn = {'new_item': [], 'cn':[]}
#     store_itemcode = []
#     item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.all()}

#     with pd.option_context('display.max_row', None):
#         selected_columns = dataframe[['Cust Code','Cust Name','Doc No','Doc Date','Doc Type','Prd Code','Prd Description','Status','Qty','UOM','Default UOM Price','Net Amt','Promo Disc Amt']]

#         for index, row in selected_columns.iterrows():
#             debtor_code = row['Cust Code']
#             debtor_name = row['Cust Name']
#             cn_no = row['Doc No']
#             cn_date = row['Doc Date']
#             doc_type = row['Doc Type']
#             item_code = row['Prd Code']
#             description = row['Prd Description']
#             doc_status = row['Status']
#             quantity = row['Qty']
#             uom = row['UOM']
#             carton_price = row['Default UOM Price']
#             net_amount = row['Net Amt']
#             discount_price = row['Promo Disc Amt']

#             if doc_type == 'CN-Prd' and doc_status == 'Confirmed':
#                 uom = 'UNT' if uom == 'PC' else 'CTN' if uom == 'CS' else uom
#                 price = carton_price if uom == 'CTN' else 0
#                 item_key = (item_code, uom)
#                 # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom=uom)
#                 if item_key not in item_uom_dict and item_key not in store_itemcode:
#                     store_itemcode.append(item_key)
#                     cn['new_item'].append({
#                         'item_code': item_code,
#                         'description': description,
#                         'uom': uom,
#                         'price': price,
#                         'rate': 0,
#                         'unit_uom': 'UNT',
#                         'unit_price': 0,
#                         'unit_rate': 1,
#                         'carton_price': carton_price,
#                         'trigger_file_type': 'CN'
#                     })

#                 cn['cn'].append({
#                     'debtor_code': debtor_code,
#                     'debtor_name': debtor_name,
#                     'cn_no': cn_no,
#                     'cn_date': cn_date,
#                     'item_code': item_code,
#                     'uom': uom,
#                     'quantity': quantity,
#                     'net_amount': net_amount,
#                     'discount_amount': discount_price
#                 })


#     return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)