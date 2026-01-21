from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
import re

def get_dksh_item_itemuom_sell(file):
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

                # if pd.isna(item_code):
                #     continue
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
                        # 'unit_uom': unit_uom,
                        # 'unit_rate':unit_rate,
                        # 'unit_price':unit_price,
                        'trigger_file_type': 'Sell'
                    })

        return JsonResponse(new_item,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_dksh_invoice_file(file):
    invoice = {'new_item': [], 'sales_invoice': []}
    dataframe = pd.read_excel(file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Invoice no','Customer code','Customer name','Salesrep code','Invoice date','Line no','Product code','Product name','Uom','Qty','Price (before dis.)','Price (after dis.)','Disc (%)','Value (w/Tax)']]
        
        # for index, row in selected_columns.iloc[:-1].iterrows():
        for index, row in selected_columns.iterrows():
            invoice_no = row['Invoice no']
            invoice_date = row['Invoice date']
            customer_code = row['Customer code']
            customer_name = row['Customer name']
            sales_agent = row['Salesrep code']
            seq = int(row['Line no'])
            item_code = int(row['Product code'])
            description = row['Product name']
            uom = row['Uom']
            quantity = row['Qty']
            price = row['Price (before dis.)']
            price_after_discount = row['Price (after dis.)']
            discount_percent = row['Disc (%)']
            net_amount = row['Value (w/Tax)']

            # print(discount_percent)
            discount_amount = round(((price*quantity)-net_amount),6)
                
            item_key =  (str(item_code), uom)
            
            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                rate = 0
                unit_uom = 'EA'
                unit_price = 0
                
                if uom == 'OUT':
                    match = re.search(r'\d+[xX]\d+', description)
                    if match:
                        extracted = match.group()
                        num1, num2 = map(int, re.split('[xX]', extracted))
                        rate = num2
                    else:
                        print("Pattern not found:", description)
                
                if uom == 'PAC':
                    unit_uom = 'PAC'
                    unit_price = price
                    rate = 1
                
                if uom == 'EA':
                    unit_uom = 'EA'
                    unit_price = price
                    rate = 1

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
                    'customer_name': customer_name,
                    'customer_code': customer_code,
                    'seq': seq,
                    'sales_agent': sales_agent,
                    'item_code': item_code,
                    'quantity': quantity,
                    'uom': uom,
                    'discount_amount': abs(discount_amount),
                    'net_amount': net_amount,
                    'description': description,
                    'price': price
            })
    
    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)

def get_dksh_cn_file(file):
    cn = {'new_item': [], 'cn': []}
    dataframe = pd.read_excel(file)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    # print(dataframe)
    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Invoice no','Customer code','Customer name','Salesrep code','Invoice date','Line no','Product code','Product name','Uom','Qty','Price (before dis.)','Price (after dis.)','Disc (%)','Value (w/Tax)']]
        
        # for index, row in selected_columns.iloc[:-1].iterrows():
        for index, row in selected_columns.iterrows():
            cn_no = row['Invoice no']
            cn_date = row['Invoice date']
            customer_code = row['Customer code']
            customer_name = row['Customer name']
            sales_agent = row['Salesrep code']
            seq = int(row['Line no'])
            item_code = int(row['Product code'])
            description = row['Product name']
            uom = row['Uom']
            quantity = row['Qty']
            # price = row['Price (before dis.)']
            price = row['Price (after dis.)']
            discount_percent = row['Disc (%)']
            net_amount = row['Value (w/Tax)']

            # price_after_discount = (price*(1 - (discount_percent/100)))
            # print(discount_percent)
            discount_amount = round(((abs(price)*abs(quantity))-abs(net_amount)),6)
                
            item_key =  (str(item_code), uom)
            
            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                rate = 0
                unit_uom = 'EA'
                unit_price = 0
                
                if uom == 'OUT':
                    match = re.search(r'\d+[xX]\d+', description)
                    if match:
                        extracted = match.group()
                        num1, num2 = map(int, re.split('[xX]', extracted))
                        rate = num2
                    else:
                        print("Pattern not found:", description)
                
                if uom == 'PAC':
                    unit_uom = 'PAC'
                    unit_price = price
                    rate = 1
                
                if uom == 'EA':
                    unit_uom = 'EA'
                    unit_price = price
                    rate = 1

                cn['new_item'].append({
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'rate': rate,
                    'price': price,
                    'unit_uom': unit_uom,
                    'unit_price': unit_price,
                    'unit_rate': 1,
                    'trigger_file_type': 'CN'
                }) 
            
            cn['cn'].append({
                    'cn_no': cn_no,
                    'cn_date': cn_date,
                    'customer_name': customer_name,
                    'customer_code': customer_code,
                    'seq': seq,
                    'sales_agent': sales_agent,
                    'item_code': item_code,
                    'description': description,
                    'quantity': abs(quantity),
                    'uom': uom,
                    'discount_amount': abs(discount_amount),
                    'net_amount': abs(net_amount),
                    'price': price
            })
    
    return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)