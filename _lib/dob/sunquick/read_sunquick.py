import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime

def process_dob_sunquick_invoice_file(dataframe):
    invoice = {'new_item': [], 'sales_invoice':[]}
    dataframe = pd.read_excel(dataframe, header=4)

    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['INVOICENO','INVOICEDATE','ACCOUNTCODE','CUSTOMERNAME','STOCKCODE','DESCRIPTION','QUANTITY','UOM','GROSSPRICE','DISCOUNT','NETPRICE','GROSSAMOUNT']]

        for index, row in selected_columns.iterrows():
            invoice_no = row['INVOICENO']
            invoice_date = row['INVOICEDATE']
            debtor_code = row['ACCOUNTCODE']
            debtor_name = row['CUSTOMERNAME']
            # sales_agent = row['PROFILE NAME']
            item_code = row['STOCKCODE']
            description = row['DESCRIPTION']
            uom = row['UOM']
            quantity = int(row['QUANTITY'])
            price = row['GROSSPRICE']
            net_price = row ['NETPRICE']
            net_amount = row['GROSSAMOUNT']
            discount_amount = row['DISCOUNT']

            item_key = (str(item_code), uom)

            # if (uom == "UNT") & (price <= 0):
            #     item = ItemUOM.objects.filter(itemcode=item_code, uom__gt=1).first()
            #     if item:
            #         rate = item.rate
            #         quantity = int(quantity/rate)
            price = abs(price)

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                if uom == 'UNT':
                    invoice['new_item'].append({
                            'item_code': item_code,
                            'description': description,
                            'uom': uom,
                            'rate': 1,
                            'price': price,
                            'unit_uom': 'UNT',
                            'unit_rate': 1,
                            'unit_price': price,
                            'trigger_file_type': 'Invoice'
                        })
                else:
                    invoice['new_item'].append({
                            'item_code': item_code,
                            'description': description,
                            'uom': uom,
                            'rate': 0,
                            'price': price,
                            'unit_uom': 'UNT',
                            'unit_rate': 1,
                            'unit_price': 0,
                            'trigger_file_type': 'Invoice'
                        })
                    
            if discount_amount>0:
                # discount_amount = quantity*discount_amount
                pass
            else:
                discount_amount = 0

            # print(invoice_no)
            invoice['sales_invoice'].append({
                    'invoice_no': invoice_no,
                    'invoice_date': invoice_date,
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    # 'sales_agent': sales_agent,
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'quantity': quantity,
                    'price': price,
                    'net_amount': net_amount,
                    'discount_amount': discount_amount
                })

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)
