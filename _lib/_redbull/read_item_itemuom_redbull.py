from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
from datetime import datetime

def get_redbull_item_itemuom_sell(file):
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
                unit_uom = row['UOM.1']
                unit_rate = row['Rate.1']
                unit_price = row['Price.1']

                # unit_uom = 'UNT' if unit_uom == 'unit' else unit_uom
                
                new_item.append({
                    'item_code': item_code,
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

def process_redbull_invoice_file(file):
    invoice = {'new_item': [], 'sales_invoice': []}
    dataframe = pd.read_excel(file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Invoice No', 'Customer Code', 'Customer Name', 'Product Code','Product Description','UOM code','Product Quantity','UOM List Price','Gross Amount','Discount Amount','Amount After SKU Disc','Transaction Date','Conversion Unit','Transaction Type','Export Date','Selling Type','Route Code']]
        
        for index, row in selected_columns.iterrows():
            invoice_no = row['Invoice No']
            invoice_date = row['Transaction Date']
            sales_agent = row['Route Code']
            delivery_date = row['Export Date']
            transaction_type = row['Transaction Type']
            customer_code = row['Customer Code']
            customer_name = row['Customer Name']
            item_code = row['Product Code']
            description = row['Product Description']
            quantity = row['Product Quantity']
            uom = row['UOM code']
            price = row['UOM List Price']
            rate = row['Conversion Unit']
            total_amount = row['Gross Amount']
            discount_amount = row['Discount Amount']
            net_amount = row['Amount After SKU Disc']
            selling_type = row['Selling Type']

            if transaction_type == 'Invoice':
                    item_key =  (str(item_code), uom)

                    # price = ctn_price if uom == 'CTN' else 0
                    # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom=uom)
                    if item_key not in item_uom_dict and item_key not in store_itemcode:
                        store_itemcode.append(item_key)
                        
                        invoice['new_item'].append({
                            'item_code': item_code,
                            'description': description,
                            'uom': uom,
                            'rate': rate,
                            'price': price,
                            'unit_uom': 'UNT',
                            'unit_price': price/rate,
                            'unit_rate': 1,
                            'trigger_file_type': 'Invoice'
                        })
                    
                    invoice['sales_invoice'].append({
                            'invoice_no': invoice_no,
                            'invoice_date': invoice_date,
                            'customer_name': customer_name,
                            'customer_code': customer_code,
                            'sales_agent': sales_agent,
                            'delivery_date': delivery_date,
                            'item_code': item_code,
                            'description': description,
                            'rate': rate,
                            'quantity': quantity,
                            'uom': uom,
                            'price': price,
                            'total_amount': total_amount,
                            'discount_amount': discount_amount,
                            'net_amount': net_amount,
                    })
    
    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)

def process_redbull_cn_file(file):
    cn = {'new_item': [], 'cn': []}
    dataframe = pd.read_excel(file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.filter(uom='CTN').select_related('itemcode')}
    
    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Uom Code','Doc No','Doc Date','Doc Type','Invoice No','Batch No','Barcode','Product Description','Qty In Ctn','Qty In Otr','Qty In Un','Unit Price','Gross Amount','Promo Discount Amount','Net Total Amount','Reason Description','Conversion to ctn','Conversion to Otr','Outlet Code','Outlet Name','Staff Code']]

        for index, row in selected_columns.iterrows():
            cn_no = row['Doc No']
            cn_date = row['Doc Date']
            doc_type = row['Doc Type']
            debtor_code = row['Outlet Code']
            debtor_name = row['Outlet Name']
            sales_agent = row['Staff Code']
            invoice_no = row['Invoice No']
            batch_no = row['Batch No']
            item_code = row['Barcode']
            description = row['Product Description']
            qty_in_ctn = row['Qty In Ctn']
            qty_in_otr = row['Qty In Otr']
            qty_in_unit = row['Qty In Un']
            price = row['Unit Price']
            total_amount = row['Gross Amount']
            discount_amount = row['Promo Discount Amount']
            net_amount = row['Net Total Amount']
            reason_description = row['Reason Description']
            ctn_rate = row['Conversion to ctn']
            otr_rate = row['Conversion to Otr']
            smallest_uom = row['Uom Code']

            if 'T' in cn_date:
                cn_date = cn_date.split('T')[0]
            elif 'M' in cn_date:
                dt = datetime.strptime(cn_date, '%d/%m/%Y %I:%M%p')
                # Convert to desired format YYYY-MM-DD
                cn_date = dt.strftime('%Y-%m-%d')
            else:
                dt = datetime.strptime(cn_date, '%d/%m/%Y')
                # Convert to desired format YYYY-MM-DD
                cn_date = dt.strftime('%Y-%m-%d')

            unit_price = price if smallest_uom == 'UNT' else 0
            ctn_price = price if smallest_uom == 'CTN' else 0
            otr_price = price if smallest_uom == 'OTR' else 0

            # print(unit_price)

            if ctn_price > 0:
                unit_price = round(ctn_price / ctn_rate,2)
                otr_price = round(otr_rate * unit_price,2)

            if otr_price > 0:
                unit_price = round(otr_price/otr_rate,2)
                ctn_price = round(unit_price*ctn_rate,2)

            if unit_price > 0:
                ctn_price = round(unit_price*ctn_rate,2)
                otr_price = round(unit_price*otr_rate,2)
            
            if doc_type == 'CN':
                item_key = (str(item_code), 'CTN')
                # is_item_exist = ItemUOM.objects.filter(itemcode=item_code,uom='CTN')
                if item_key not in item_uom_dict and item_key not in store_itemcode:
                    store_itemcode.append(item_key)
                    cn['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'carton_uom': 'CTN',
                        'carton_rate': ctn_rate,
                        'carton_price': ctn_price,
                        'otr_uom': 'OTR',
                        'otr_rate': otr_rate,
                        'otr_price': otr_price,
                        'unit_uom': 'UNT',
                        'rate': 1,
                        'unit_price': unit_price,
                        'trigger_file_type': 'CN'
                    })

                cn['cn'].append({
                    'cn_no': cn_no,
                    'cn_date': cn_date,
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'sales_agent': sales_agent,
                    'invoice_no': invoice_no,
                    'batch_no': batch_no,
                    'item_code': item_code,
                    'description': description,
                    'qty_in_ctn': qty_in_ctn,
                    'carton_rate': ctn_rate,
                    'carton_uom': 'CTN',
                    'qty_in_otr': qty_in_otr,
                    'otr_rate': otr_rate,
                    'otr_uom': 'OTR',
                    'qty_in_unit': qty_in_unit,
                    'unit_rate': 1,
                    'unit_uom': 'UNT',
                    'carton_price': ctn_price,
                    'otr_price': otr_price,
                    'unit_price': unit_price,
                    'discount_amount': discount_amount,
                    'net_amount': net_amount,
                    'reason_description': reason_description,
                })

    return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)