from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
import math
import datetime

def process_dob_tohtonku_invoice_file(file):
    invoice = {'new_item': [], 'sales_invoice': []}
    dataframe = pd.read_excel(file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}
    
    def excel_date_to_datetime(excel_date):
        if pd.isna(excel_date):
            return None
            
        # Check if it's already a datetime (pandas might auto-convert)
        if isinstance(excel_date, (datetime.datetime, datetime.date)):
            return excel_date
            
        # For numeric Excel dates
        try:
            # Excel dates start from January 1, 1900
            excel_epoch = datetime.datetime(1899, 12, 30)  # This accounts for the leap year bug
            
            # Convert Excel date to a Python datetime
            dt = excel_epoch + datetime.timedelta(days=int(excel_date))
            return dt
        except (ValueError, TypeError):
            # If conversion fails, return None or original value
            return excel_date

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['DocumentNo', 'CustomerCode','GrossAmount', 'CustomerName', 'StockCode','Description','Uom','Quantity','GrossPrice','DiscAmount1','NetAmount','DocumentDate','BaseQuantity','DocumentType']]
        
        for index, row in selected_columns.iterrows():
            invoice_no = row['DocumentNo']
            
            raw_invoice_date = row['DocumentDate']
            invoice_date = excel_date_to_datetime(raw_invoice_date)
            invoice_date = invoice_date.date()

            transaction_type = row['DocumentType']
            customer_code = row['CustomerCode']
            customer_name = row['CustomerName']
            item_code = row['StockCode']
            description = row['Description']
            quantity = row['Quantity']
            uom = row['Uom']
            price = row['GrossPrice'] 
            rate = row['BaseQuantity']
            total_amount = row['GrossAmount']
            discount_amount = row['DiscAmount1']
            net_amount = row['NetAmount']

            
            item_key =  (str(item_code), uom)
            if item_key not in item_uom_dict and item_key not in store_itemcode:
                
                store_itemcode.append(item_key)
                
                if uom == 'CTN':
                    unit_price = round((price/rate),2)
                    invoice['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': uom,
                        'rate': rate,
                        'price': price,
                        'unit_uom': 'UNIT',
                        'unit_price': unit_price,
                        'unit_rate': 1,
                        'trigger_file_type': 'Invoice'
                    })
                elif uom == 'UNIT':
                     invoice['new_item'].append({
                        'item_code': item_code,
                        'description': description,
                        'uom': 'UNIT',
                        'rate': 1,
                        'price': price,
                        'unit_uom': 'UNIT',
                        'unit_price': price,
                        'unit_rate': 1,
                        'trigger_file_type': 'Invoice'
                    })
            
            if not customer_code:
                 return JsonResponse('empty debtor code', safe=False, status=status.HTTP_404_NOT_FOUND)
            
            invoice['sales_invoice'].append({
                    'invoice_no': invoice_no,
                    'invoice_date': invoice_date,
                    'customer_name': customer_name,
                    'customer_code': customer_code,
                    # 'sales_agent': sales_agent,
                    # 'delivery_date': delivery_date,
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
