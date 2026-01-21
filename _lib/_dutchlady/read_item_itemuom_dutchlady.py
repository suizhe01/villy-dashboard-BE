from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
from company.models import Company
from item.models import Item
from datetime import datetime
import math

def get_dutchlady_item_itemuom_sell(file):
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
                        'trigger_file_type': 'Sell'
                    })

        return JsonResponse(new_item,safe=False, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def process_dutchlady_invoice_file(uploaded_file):
    sales = {'new_item':[],'sales_invoice':[]}
    dataframe = pd.read_excel(uploaded_file)
    store_itemcode = []
    # itemuom_list = ItemUOM.objects.filter(uom='BOX').values('itemcode_id')
    # itemuom_list = list(itemuom_list.values())
    # print(type(itemuom_list))
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}


    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['transaction_type', 'customer_code', 'customer_name', 'transaction_no','transaction_date','product_code','productdesc','conversion_unit','box_price','box_qty','piece_qty','sum of promotion discount','total_price','net amount - before round off','salesman code']]

        for index, row in selected_columns.iterrows():
            debtor_code = row['customer_code']
            debtor_name = row['customer_name']
            transaction_type = row['transaction_type']
            transaction_no = row['transaction_no']
            item_code = row['product_code']
            description = row['productdesc']
            transaction_date = row['transaction_date']
            box_qty = row['box_qty']
            unit_qty = row['piece_qty']
            price = row['box_price']
            rate = row['conversion_unit']
            total_price = row['total_price'] # is qualt to total_amount header
            sales_agent = row['salesman code']
            discount_amt = row['sum of promotion discount']
            net_amount = row['net amount - before round off']

            
            
            if transaction_type == 'sales':
                if math.isnan(discount_amt):
                    discount_amt = float(0)
                
                print(total_price)
                # piece_price = 0 
                # if box_qty>0:
                #     if unit_qty>0:
                #         piece_price = (net_amount-(box_qty*price))/unit_qty
                # else:
                #     piece_price = net_amount/unit_qty
                piece_price = price/rate
                item_key = (str(item_code),'BOX')

                if item_key not in item_uom_dict and item_key not in store_itemcode:
                    store_itemcode.append((item_code,'BOX'))
                    sales['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': 'BOX',
                        'price': price,
                        'rate': rate,
                        'unit_uom': 'unit',
                        'unit_price': piece_price,
                        'unit_rate': 1,
                        'trigger_file_type': 'Invoice'
                    })
                

                sales['sales_invoice'].append({
                        'debtor_code': debtor_code,
                        'debtor_name': debtor_name,
                        'transaction_type': transaction_type,
                        'transaction_no': transaction_no,
                        'transaction_date': transaction_date,
                        'description': description,
                        'item_code': item_code,
                        'box_qty': box_qty,
                        'rate': rate,
                        'uom': 'BOX',
                        'unit_qty': unit_qty,
                        'unit_rate': 1,
                        'unit_uom': 'unit',
                        'total_price': total_price,
                        'sales_agent': sales_agent,
                        'discount_amt': discount_amt,
                        'net_amt': net_amount,
                        'box_price': price,
                        'piece_price': piece_price
                })

    return JsonResponse(sales, safe=False, status=status.HTTP_200_OK)

def process_dutchlady_cn_file(uploaded_file):
    cn = {'new_item':[],'cn':[]}
    dataframe = pd.read_excel(uploaded_file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}
    error = {"error": "contain empty cn number"}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['transaction_type','salesman code','customer_code','customer_name','transaction_date','credit note no','product_code','productdesc','conversion_unit','box_price','box_qty','piece_qty','total_price','remarks','promotion discount']]
        for index, row in selected_columns.iterrows():
            transaction_type = row['transaction_type']
            sales_man = row['salesman code']
            debtor_code = row['customer_code']
            debtor_name = row['customer_name']
            cn_no = row['credit note no']
            cn_date = row['transaction_date']
            item_code = row['product_code']
            description = row['productdesc']
            rate = row['conversion_unit']
            price = row['box_price']
            box_qty = row['box_qty']
            unit_qty = row['piece_qty']
            discount_amount = row['promotion discount']
            total_amount = row['total_price']
            net_amount = row['total_price']
            our_invoice_no = row['remarks']

            # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom='BOX')
            
            if transaction_type == 'Credit Note':
                piece_price = round(price/rate,4)
                item_key = (str(item_code), 'BOX')

                if pd.isna(cn_no):
                    return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)

                if item_key not in item_uom_dict and item_key not in store_itemcode:
                    store_itemcode.append(item_key)

                    cn['new_item'].append({
                        'item_code' : item_code,
                        'description' : description,
                        'uom' : 'BOX',
                        'price' : price,
                        'rate' : rate,
                        'unit_uom' : 'unit',
                        'unit_price' : piece_price,
                        'unit_rate' : 1,
                        'trigger_file_type': 'CN'
                    })

                if pd.isna(our_invoice_no):
                    our_invoice_no = ''
                
                cn['cn'].append({
                        'cn_no':cn_no,
                        'cn_date':cn_date,
                        'debtor_code':debtor_code,
                        'debtor_name':debtor_name,
                        'sales_man' :sales_man,
                        'item_code': item_code,
                        'description': description,
                        'box_qty':box_qty,
                        'box_rate': rate,
                        'box_uom': 'BOX',
                        'piece_qty':unit_qty,
                        'unit_rate': 1,
                        'unit_uom': 'unit',
                        'total_amount':abs(total_amount),
                        'discount_amount':abs(discount_amount),
                        'net_amount': abs(net_amount),
                        'box_price': price,
                        'unit_price': piece_price,
                        'our_invoice_no': our_invoice_no
                    })
                
                # if discount_amount is not None and not math.isnan(discount_amount):
                #     cn['cn'].append({
                #         'cn_no':cn_no,
                #         'cn_date':cn_date,
                #         'debtor_code':debtor_code,
                #         'debtor_name':debtor_name,
                #         'sales_man' :sales_man,
                #         'item_code': item_code,
                #         'description': description,
                #         'box_qty':box_qty,
                #         'box_rate': rate,
                #         'box_uom': 'BOX',
                #         'piece_qty':unit_qty,
                #         'unit_rate': 1,
                #         'unit_uom': 'unit',
                #         'total_amount':total_amount,
                #         'discount_amount':discount_amount,
                #         'net_amount': abs(net_amount),
                #         'box_price': price,
                #         'unit_price': piece_price
                #     })
                # else:
                #     cn['cn'].append({
                #         'cn_no':cn_no,
                #         'cn_date':cn_date,
                #         'debtor_code':debtor_code,
                #         'debtor_name':debtor_name,
                #         'sales_man' :sales_man,
                #         'item_code': item_code,
                #         'description': description,
                #         'box_qty':box_qty,
                #         'box_rate': rate,
                #         'box_uom': 'BOX',
                #         'piece_qty':unit_qty,
                #         'unit_rate': 1,
                #         'unit_uom': 'unit',
                #         'total_amount':total_amount,
                #         'discount_amount':0,
                #         'net_amount': abs(net_amount),
                #         'box_price': price,
                #         'unit_price': piece_price
                #     })


    return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)

