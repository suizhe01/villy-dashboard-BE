import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime
import re

def process_dob_dksh_invoice_file(dataframe):
    invoice = {'new_item': [], 'sales_invoice': []}
    dataframe = pd.read_excel(dataframe)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    # DKSH only writes the invoice columns on the first line of each invoice and
    # leaves them blank on its remaining lines, so fill them down. Any row still
    # blank afterwards sits above the first invoice in the file and is skipped.
    header_columns = ['Inv No','Inv Date','Ship-To','Ship-To Name']
    dataframe[header_columns] = dataframe[header_columns].ffill()

    with pd.option_context('display.max_row', None):
        print(f"[dob_dksh] Total rows: {len(dataframe)}")
        selected_columns = dataframe[['Inv No','Inv Date','Ship-To','Ship-To Name','ItemCode','ItemDescription','UOM','Qty','UnitPrice','Discount','TotalPrice']]

        previous_invoice_no = ''
        seq = 0

        for index, row in selected_columns.iterrows():
            if pd.isna(row['Inv No']) or pd.isna(row['ItemCode']):
                continue

            invoice_no = int(row['Inv No'])

            if invoice_no != previous_invoice_no:
                previous_invoice_no = invoice_no
                seq = 1
            else:
                seq += 1

            invoice_date = pd.to_datetime(row['Inv Date']).strftime('%Y-%m-%dT%H:%M:%S')
            debtor_code = int(row['Ship-To'])
            debtor_name = str(row['Ship-To Name']).strip()
            item_code = int(row['ItemCode'])
            description = str(row['ItemDescription']).strip()
            uom = str(row['UOM']).strip()
            quantity = int(row['Qty'])
            price = round(float(row['UnitPrice']), 6)
            net_amount = round(float(row['TotalPrice']), 6)

            discount_amount = 0 if pd.isna(row['Discount']) else float(row['Discount'])
            if discount_amount == 0:
                discount_amount = round(((price * quantity) - net_amount), 6)

            item_key = (str(item_code), uom)

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                # Base units carry their own price and need no second row. Any
                # larger UOM (OUT, CAR, ...) pairs with an EA row at rate 1, and
                # falls back to rate 1 when the pack factor is unknown - never 0,
                # which would divide by zero when posting smallestunitprice.
                rate = 1
                unit_uom = 'EA'
                unit_price = 0

                if uom in ('EA', 'PAC'):
                    unit_uom = uom
                    unit_price = price
                elif uom == 'OUT':
                    match = re.search(r'\d+[xX]\d+', description)
                    if match:
                        num1, num2 = map(int, re.split('[xX]', match.group()))
                        rate = num2
                    else:
                        print(f"[dob_dksh] Pack factor not found, rate defaults to 1: {item_code} {uom} {description}")
                else:
                    print(f"[dob_dksh] Unmapped UOM, rate defaults to 1: {item_code} {uom} {description}")

                invoice['new_item'].append({
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'rate': rate,
                    'price': price,
                    'unit_uom': unit_uom,
                    'unit_price': unit_price,
                    'unit_rate': 1,
                    'trigger_file_type': 'Invoice'
                })

            invoice['sales_invoice'].append({
                'invoice_no': invoice_no,
                'invoice_date': invoice_date,
                'seq': seq,
                'debtor_code': debtor_code,
                'debtor_name': debtor_name,
                'sales_agent': 'NA',
                'item_code': item_code,
                'description': description,
                'quantity': quantity,
                'uom': uom,
                'price': price,
                'discount_amount': abs(discount_amount),
                'net_amount': net_amount,
            })

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)
