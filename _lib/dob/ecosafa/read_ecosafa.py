import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime

def process_dob_ecosafa_invoice_file(dataframe):
    invoice = {'new_item': [], 'sales_invoice': []}
    dataframe = pd.read_excel(dataframe, header=4)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        print(f"[ecosafa] Total rows: {len(dataframe)}")
        selected_columns = dataframe[['INVOICE NO', 'INVOICE DATE', 'DEBTOR CODE', 'BUYER ', 'ITEM CODE', 'ITEM ', 'SIZE', 'QUANITTY (CTNS)', 'UOM']]

        for index, row in selected_columns.iterrows():
            if pd.isna(row['INVOICE NO']) or pd.isna(row['ITEM CODE']):
                continue

            invoice_no = int(row['INVOICE NO'])
            raw_date = str(row['INVOICE DATE'])
            try:
                invoice_date = datetime.strptime(raw_date, '%d.%m.%Y').strftime('%Y-%m-%dT%H:%M:%S')
            except ValueError:
                invoice_date = datetime.strptime(raw_date, '%d.%m.%y').strftime('%Y-%m-%dT%H:%M:%S')
            debtor_code = row['DEBTOR CODE']
            debtor_name = str(row['BUYER ']).strip()
            item_code = row['ITEM CODE']
            description = str(row['ITEM ']).strip()
            size = row['SIZE']
            quantity = row['QUANITTY (CTNS)']
            uom = row['UOM']

            try:
                ctn_rate = int(str(size).split('X')[0].strip())
            except (ValueError, IndexError):
                ctn_rate = 1

            item_key = (str(item_code), str(uom))

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                invoice['new_item'].append({
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'rate': ctn_rate,
                    'price': 0,
                    'unit_uom': 'UNIT',
                    'unit_rate': 1,
                    'unit_price': 0,
                    'trigger_file_type': 'Invoice'
                })

            invoice['sales_invoice'].append({
                'invoice_no': invoice_no,
                'invoice_date': invoice_date,
                'debtor_code': debtor_code,
                'debtor_name': debtor_name,
                'item_code': item_code,
                'description': description,
                'rate': ctn_rate,
                'quantity': quantity,
                'uom': uom,
            })

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)
