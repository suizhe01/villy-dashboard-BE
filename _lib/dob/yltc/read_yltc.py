from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
import math

def process_dob_yltc_invoice_file(file):
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

            if isinstance(customer_code, (int, float)):  # Ensure it's a number
                if math.isnan(customer_code):  # Check if it's NaN
                    return JsonResponse('empty debtor code', safe=False, status=status.HTTP_404_NOT_FOUND)
            elif not customer_code or customer_code.strip() == "":  # Check if it's empty or just spaces
                return JsonResponse('empty debtor code', safe=False, status=status.HTTP_404_NOT_FOUND)
            
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
                            'unit_price': round((price/rate),2),
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