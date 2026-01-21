from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
import math

def get_cola_item_itemuom_sell(file):
    try:
        new_item = []
        dataframe = pd.read_excel(file, header=2,sheet_name=1)
        store_itemcode = []

        with pd.option_context('display.max_row', None):
            selected_columns = dataframe[['ItemCode','Description','UOM','Rate','Price','UOM.1','Rate.1','Price.1']]

            for index, row in selected_columns.iterrows():
                item_code= row['ItemCode']
                description = row['Description']
                uom = row['UOM']
                rate = row['Rate']
                price = row['Price']
                # unit_uom = row['UOM.1']
                # unit_rate = row['Rate.1']
                # unit_price = row['Price.1']
                unit_uom = 'unit'
                unit_rate = 1
                unit_price = price/rate

                if pd.isna(item_code):
                    continue
                # unit_uom = 'UNT' if unit_uom == 'unit' else unit_uom
                
                item_key = (item_code,uom)
                if item_key not in store_itemcode:
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

def process_cola_invoice_file(uploaded_file):
    invoice = {'new_item': [], 'sales_invoice': []}
    dataframe = pd.read_excel(uploaded_file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    if pd.api.types.is_integer_dtype(dataframe['DELDAT']):
        # Convert the integer dates to datetime
        dataframe['DELDAT'] = pd.to_datetime(dataframe['DELDAT'], origin='1899-12-30', unit='D')

    with pd.option_context('display.max_row', None):
        # article no = item code 
        selected_cola_columns = dataframe[['DOCNUM','MEP_CUSTOMER_NO','SHIPTO_NAME1','ENTRYSEQ','ARTNUM','ARTNAM','DELDAT','PRI','INV_TOTAL','ADJ_FINPRI','ADJAMT','TOTALQTY_WITH_FREECASE','NUMSUU','SALMANNUM','EWALLET']]
                                
        for index, row in selected_cola_columns.iterrows():
            invoice_no = row['DOCNUM']
            invoice_date = row['DELDAT']
            debtor_code = row['MEP_CUSTOMER_NO']
            debtor_name = row['SHIPTO_NAME1']
            sales_agent = row['SALMANNUM']
            seq = row['ENTRYSEQ']
            item_code = row['ARTNUM']
            rate = row['NUMSUU']
            price = row['PRI']
            description = row['ARTNAM']
            quantity = row['TOTALQTY_WITH_FREECASE']
            total_inv_amount = row['INV_TOTAL']
            discount_amount = row['ADJAMT']
            net_amount = row['ADJ_FINPRI']
            ewallet = row['EWALLET']
            
            item_key = (str(item_code),'CTN')

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                invoice['new_item'].append({
                    'item_code': item_code,
                    'description': description,
                    'uom': 'CTN',
                    'rate': rate,
                    'price': price,
                    'unit_uom': 'UNT',
                    'unit_rate': 1,
                    'unit_price': 1,
                    'trigger_file_type': 'Invoice'
                })
            
            if math.isnan(discount_amount):
                discount_amount = 0
            else:
                discount_amount = abs(discount_amount)
            
            invoice['sales_invoice'].append({
                'invoice_no': invoice_no,
                'invoice_date': invoice_date,
                'debtor_name': debtor_name,
                'debtor_code': debtor_code,
                'sales_agent': sales_agent,
                'seq': seq,
                'item_code': item_code,
                'quantity': quantity,
                'uom': 'CTN',
                'discount_amount': discount_amount,
                'net_amount': net_amount,
                'description': description,
                'price': price,
                'rate': rate,
                'total_invoice_amount': total_inv_amount,
                'ewallet': ewallet
            })

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)

def process_cola_cn_file(uploaded_file):
    invoice = {'new_item': [], 'cn': []}
    dataframe = pd.read_excel(uploaded_file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    if pd.api.types.is_integer_dtype(dataframe['DELDAT']):
        # Convert the integer dates to datetime
        dataframe['DELDAT'] = pd.to_datetime(dataframe['DELDAT'], origin='1899-12-30', unit='D')
        
    with pd.option_context('display.max_row', None):
        # article no = item code 
        selected_cola_columns = dataframe[['DOCNUM','MEP_CUSTOMER_NO','SHIPTO_NAME1','ENTRYSEQ','ARTNUM','ARTNAM','DELDAT','PRI','INV_TOTAL','ADJ_FINPRI','ADJAMT','TOTALQTY_WITH_FREECASE','NUMSUU','SALMANNUM','EWALLET']]
                                
        for index, row in selected_cola_columns.iterrows():
            cn_no = row['DOCNUM']
            cn_date = row['DELDAT']
            debtor_code = row['MEP_CUSTOMER_NO']
            debtor_name = row['SHIPTO_NAME1']
            sales_agent = row['SALMANNUM']
            seq = row['ENTRYSEQ']
            item_code = row['ARTNUM']
            rate = row['NUMSUU']
            price = row['PRI']
            description = row['ARTNAM']
            quantity = row['TOTALQTY_WITH_FREECASE']
            total_inv_amount = row['INV_TOTAL']
            discount_amount = row['ADJAMT']
            net_amount = row['ADJ_FINPRI']
            ewallet = row['EWALLET']

            
            item_key = (str(item_code),'CTN')

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                invoice['new_item'].append({
                    'item_code': item_code,
                    'description': description,
                    'uom': 'CTN',
                    'rate': rate,
                    'price': price,
                    'unit_uom': 'UNT',
                    'unit_rate': 1,
                    'unit_price': 1,
                    'trigger_file_type': 'Invoice'
                })
            
            if math.isnan(discount_amount):
                discount_amount = 0
            else:
                discount_amount = abs(discount_amount)
            
            invoice['cn'].append({
                'cn_no': cn_no,
                'cn_date': cn_date,
                'debtor_name': debtor_name,
                'debtor_code': debtor_code,
                'sales_agent': sales_agent,
                'seq': seq,
                'item_code': item_code,
                'description': description,
                'quantity': abs(quantity),
                'uom': 'CTN',
                'discount_amount': discount_amount,
                'net_amount': abs(net_amount),
                'rate': rate,
                'uom': 'CTN',
                'price': price,
                'total_invoice_amount': abs(total_inv_amount),
                'ewallet': abs(ewallet)
            })

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)