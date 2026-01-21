from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM

def get_lipton_item_itemuom_sell(file):
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

                if pd.isna(item_code):
                    continue
                # unit_uom = 'UNT' if unit_uom == 'unit' else unit_uom
                
                item_key = (str(int(item_code)), uom)
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


def process_lipton_invoice_file(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    invoice = {'new_item': [], 'sales_invoice':[]}
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}
    # print(datetime.now())
    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Cust Code','Cust Name','Doc No','Doc Date','Doc Type','Status','Prd Code','Prd Description','Qty','UOM','Default UOM Price','Net Amt','Promo Disc Amt','Route Code']]

        for index, row in selected_columns.iterrows():
            debtor_code = row['Cust Code']
            debtor_name = row['Cust Name']
            sales_agent = row['Route Code']
            invoice_no = row['Doc No']
            invoice_date = row['Doc Date']
            doc_type = row['Doc Type']
            doc_status = row['Status']
            item_code = row['Prd Code']
            description = row['Prd Description']
            quantity = row['Qty']
            uom = row['UOM']
            carton_price = row['Default UOM Price']
            net_amount = row['Net Amt']
            discount_amount = row['Promo Disc Amt']

            if doc_type == 'Inv' and doc_status == 'Confirmed':
                price = carton_price if uom == 'CS' else 0
                rate = 1 if uom == 'PC' else 0
                item_key = (str(item_code), uom)
                # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom=uom)
                if item_key not in item_uom_dict and item_key not in store_itemcode:
                    store_itemcode.append(item_key)
                    invoice['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': uom,
                        'price': price,
                        'rate': rate,
                        'unit_uom': 'PC',
                        'unit_price': 0,
                        'unit_rate': 1,
                        'carton_price': carton_price,
                        'trigger_file_type': 'Invoice'
                })
                    
                invoice['sales_invoice'].append({
                    'debtor_code': debtor_code,
                    'debtor_name':debtor_name,
                    'sales_agent': sales_agent,
                    'invoice_no': invoice_no,
                    'invoice_date': invoice_date,
                    'net_amount':net_amount,
                    'discount_amount': discount_amount,
                    'quantity': quantity,
                    'description': description,
                    'item_code': item_code,
                    'price': net_amount/quantity,
                    'uom': uom
                })
    # print(datetime.now())

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)

def process_lipton_cn_file(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    cn = {'new_item': [], 'cn':[]}
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Route Code','Cust Code','Cust Name','Doc No','Doc Date','Doc Type','Prd Code','Prd Description','Status','Qty','UOM','Default UOM Price','Net Amt','Promo Disc Amt']]

        for index, row in selected_columns.iterrows():
            debtor_code = row['Cust Code']
            debtor_name = row['Cust Name']
            sales_agent = row['Route Code']
            cn_no = row['Doc No']
            cn_date = row['Doc Date']
            doc_type = row['Doc Type']
            item_code = row['Prd Code']
            description = row['Prd Description']
            doc_status = row['Status']
            quantity = row['Qty']
            uom = row['UOM']
            carton_price = row['Default UOM Price']
            net_amount = row['Net Amt']
            discount_price = row['Promo Disc Amt']

            if doc_type == 'CN-Prd' and doc_status == 'Confirmed':
                price = carton_price if uom == 'CS' else 0
                rate = 1 if uom =='PC' else 0
                item_key = (str(item_code), uom)
                # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom=uom)
                if item_key not in item_uom_dict and item_key not in store_itemcode:
                    store_itemcode.append(item_key)
                    cn['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': uom,
                        'price': price,
                        'rate': rate,
                        'unit_uom': 'PC',
                        'unit_price': 0,
                        'unit_rate': 1,
                        'carton_price': carton_price,
                        'trigger_file_type': 'CN'
                    })

                cn['cn'].append({
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'sales_agent': sales_agent,
                    'cn_no': cn_no,
                    'cn_date': cn_date,
                    'item_code': item_code,
                    'description': description,
                    'price': net_amount/quantity,
                    'uom': uom,
                    # 'rate': rate,
                    'quantity': quantity,
                    'net_amount': net_amount,
                    'discount_amount': discount_price
                })


    return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)