import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
import math
from decimal import Decimal
from datetime import datetime
import json

def process_dutchlady_purchase_file(uploaded_file):
    purchase = {'new_item':[],'purchase_invoice':[]}
    dataframe = pd.read_excel(uploaded_file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom, item.cost): item for item in ItemUOM.objects.all()}
    
    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['product_code', 'product_desc', 'uom','primary_product_received_qty(box)', 'primary_product_price','primary_delivery_no','grn_date','primary_invoice_no','primary_invoice_date','product_batch','primary_net_amount','primary_product_expiry_date']]
        
        for index, row in selected_columns.iterrows():
            item_code = row['product_code']
            description = row['product_desc']
            uom = row['uom']
            quantity = row['primary_product_received_qty(box)']
            price = row['primary_product_price']
            good_receive_no = row['primary_delivery_no']
            good_receive_date = row['grn_date']
            invoice_no = row['primary_invoice_no']
            invoice_date = row['primary_invoice_date']
            batch = row['product_batch']
            net_amount = row['primary_net_amount']
            product_expiry_date = row['primary_product_expiry_date']
            
            # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom=uom)
            item_key = (item_code, uom)
            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                purchase['new_item'].append({
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'price': price,
                    'rate': 0,
                    'unit_uom': 'UNT',
                    'unit_price': 0,
                    'unit_rate': 1,
                    'trigger_file_type': 'Purchase'
                })
                # print(store_itemcode)
            
            purchase['purchase_invoice'].append({
                "purchase_invoice_no": invoice_no,
                'purchase_invoice_date': invoice_date,
                'good_receive_no': good_receive_no,
                'good_receive_date': good_receive_date,
                'batch': batch,
                'product_expiry_date': product_expiry_date,
                'quantity': quantity,
                'net_amount': net_amount,
                'item_code': item_code,
                'uom': uom
            })

    return JsonResponse(purchase, safe=False, status=status.HTTP_200_OK)

# def process_dutchlady_invoice_file(uploaded_file):
#     sales = {'new_item':[],'sales':[]}
#     dataframe = pd.read_excel(uploaded_file)
#     store_itemcode = []
#     # itemuom_list = ItemUOM.objects.filter(uom='BOX').values('itemcode_id')
#     # itemuom_list = list(itemuom_list.values())
#     # print(type(itemuom_list))
#     item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.filter(uom='BOX')}

#     with pd.option_context('display.max_row', None):
#         selected_columns = dataframe[['transaction_type', 'customer_code', 'customer_name', 'transaction_no','transaction_date','product_code','productdesc','conversion_unit','box_price','total_price','box_qty','piece_qty','total item discount - before tax','total line net amount','total amount after discount invoice level','salesman code']]

#         for index, row in selected_columns.iterrows():
#             debtor_code = row['customer_code']
#             debtor_name = row['customer_name']
#             transaction_type = row['transaction_type']
#             transaction_no = row['transaction_no']
#             item_code = row['product_code']
#             description = row['productdesc']
#             transaction_date = row['transaction_date']
#             box_qty = row['box_qty']
#             unit_qty = row['piece_qty']
#             price = row['box_price']
#             rate = row['conversion_unit']
#             total_price = row['total line net amount']
#             sales_agent = row['salesman code']
#             discount_amt = row['total item discount - before tax']
#             net_amount = row['total amount after discount invoice level']
            
#             # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom='BOX')
#             # is_item_exist = any(d['itemcode_id'] == item_code for d in itemuom_list)
#             item_key = (item_code,'BOX')
#             if transaction_type == 'sales':
#                 if item_key not in item_uom_dict and item_key not in store_itemcode:
#                     store_itemcode.append((item_code,'BOX'))
#                     sales['new_item'].append({
#                         'item_code': item_code,
#                         'description': description,
#                         'uom': 'BOX',
#                         'price': price,
#                         'rate': rate,
#                         'unit_uom': 'UNT',
#                         'unit_price': 0,
#                         'unit_rate': 1,
#                         'trigger_file_type': 'Invoice'
#                     })

#                 sales['sales'].append({
#                         'debtor_code': debtor_code,
#                         'debtor_name': debtor_name,
#                         'transaction_type': transaction_type,
#                         'transaction_no': transaction_no,
#                         'transaction_date': transaction_date,
#                         'item_code': item_code,
#                         'box_qty': box_qty,
#                         'unit_qty': unit_qty,
#                         'total_price': total_price,
#                         'sales_agent': sales_agent,
#                         'discount_amt': discount_amt,
#                         'net_amt': net_amount
#                 })

#     return JsonResponse(sales, safe=False, status=status.HTTP_200_OK)

# def process_dutchlady_cn_file(uploaded_file):
#     cn = {'new_item':[],'cn':[]}
#     dataframe = pd.read_excel(uploaded_file)
#     store_itemcode = []
#     item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.all()}
#     error = {"error": "contain empty cn number"}

#     with pd.option_context('display.max_row', None):
#         selected_columns = dataframe[['transaction_type','salesman code','customer_code','customer_name','transaction_date','credit note no','product_code','productdesc','conversion_unit','box_price','box_qty','piece_qty','total item discount - before tax','total line net amount','total amount after discount invoice level']]
#         for index, row in selected_columns.iterrows():
#             transaction_type = row['transaction_type']
#             sales_man = row['salesman code']
#             debtor_code = row['customer_code']
#             debtor_name = row['customer_name']
#             cn_no = row['credit note no']
#             cn_date = row['transaction_date']
#             item_code = row['product_code']
#             description = row['productdesc']
#             rate = row['conversion_unit']
#             price = row['box_price']
#             box_qty = row['box_qty']
#             peice_qty = row['piece_qty']
#             discount_amount = row['total item discount - before tax']
#             total_amount = row['total line net amount']
#             net_amount = row['total amount after discount invoice level']

#             # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom='BOX')
#             item_key = (item_code, 'BOX')
#             if transaction_type == 'Credit Note':
#                 if pd.isna(cn_no):
#                     return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
#                 if item_key not in item_uom_dict and item_key not in store_itemcode:
#                     store_itemcode.append(item_key)
#                     cn['new_item'].append({
#                         'item_code' : item_code,
#                         'description' : description,
#                         'uom' : 'BOX',
#                         'price' : price,
#                         'rate' : rate,
#                         'unit_uom' : 'UNT',
#                         'unit_price' : 0,
#                         'unit_rate' : 1,
#                         'trigger_file_type': 'CN'
#                     })
                
#                 if discount_amount is not None and not math.isnan(discount_amount):
#                     cn['cn'].append({
#                         'cn_no':cn_no,
#                         'cn_date':cn_date,
#                         'debtor_code':debtor_code,
#                         'debtor_name':debtor_name,
#                         'sales_man' :sales_man,
#                         'item_code': item_code,
#                         'box_qty':box_qty,
#                         'piece_qty':peice_qty,
#                         'total_amount':total_amount,
#                         'discount_amount':discount_amount,
#                         'net_amount': abs(net_amount)
#                     })
#                 else:
#                     cn['cn'].append({
#                         'cn_no':cn_no,
#                         'cn_date':cn_date,
#                         'debtor_code':debtor_code,
#                         'debtor_name':debtor_name,
#                         'sales_man' :sales_man,
#                         'item_code': item_code,
#                         'box_qty':box_qty,
#                         'piece_qty':peice_qty,
#                         'total_amount':total_amount,
#                         'discount_amount':0,
#                         'net_amount': abs(net_amount)
#                     })


#     return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)