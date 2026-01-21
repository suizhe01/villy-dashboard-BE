import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime

def process_mp_itemcode_file(dataframe):
    new_item = {'new_item' : []}
    dataframe = pd.read_excel(dataframe, sheet_name=None)

    # Check if both 'DSG' and 'UCM' sheets exist in the file
    if "DSG" in dataframe and "UCM" in dataframe:
        # Read only the 'DSG' and 'UCM' sheets
        dsg_df = dataframe["DSG"]
        ucm_df = dataframe["UCM"]
        
        # Concatenate the two DataFrames
        dataframe = pd.concat([dsg_df, ucm_df], ignore_index=True)
    # dataframe = pd.read_excel(dataframe, sheet_name=["DSG","UCM"])
    # dataframe = pd.concat([dataframe["DSG"], dataframe["UCM"]], ignore_index=True)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Product code','Product name','SIZE','COST']]

        for index, row in selected_columns.iterrows():
            item_code = row['Product code']
            description = row['Product name']
            rate = row['SIZE']
            price = row['COST']

            item_key = (str(item_code),'Carton')
            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)

                new_item['new_item'].append({
                    'item_code': item_code,
                    'description': description,
                    'rate': rate,
                    'price': price,
                    'uom': 'Carton',
                    'unit_uom': 'Unit',
                    'unit_rate': 1,
                    'unit_price': price/rate,
                    'trigger_file_type': 'AddItem'
                })

    return JsonResponse(new_item, safe=False, status=status.HTTP_200_OK)

def process_mp_invoice_file(dataframe):
    invoice = {'new_item': [], 'sales_invoice':[]}
    dataframe = pd.read_excel(dataframe, header=3)

    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['INV DATE','INV NO','CUST ID','CUSTOMER NAME','PROFILE NAME','SKU NO','SKU DESCRIPTION','UOM','QTY CTN','QTY IN EA','LIST PRICE CTN','LIST PRICE IN EA','TOTAL AMT BEFORE TAX','TOTAL DISC AMT']]

        for index, row in selected_columns.iterrows():
            invoice_no = row['INV NO']
            invoice_date = row['INV DATE']
            debtor_code = row['CUST ID']
            debtor_name = row['CUSTOMER NAME']
            sales_agent = row['PROFILE NAME']
            item_code = row['SKU NO']
            description = row['SKU DESCRIPTION']
            uom = row['UOM']
            carton_qty = row['QTY CTN']
            carton_price = row['LIST PRICE CTN']
            unit_qty = row['QTY IN EA']
            unit_price = row['LIST PRICE IN EA']
            net_amount = row['TOTAL AMT BEFORE TAX']
            discount_amount = row['TOTAL DISC AMT']

            item_key = (str(item_code), uom)

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                if uom == 'Carton':
                    invoice['new_item'].append({
                            'item_code': item_code,
                            'description': description,
                            'uom': uom,
                            'rate': 1,
                            'price': carton_price,
                            'unit_uom': 'Unit',
                            'unit_rate': 1,
                            'unit_price': 0,
                            'trigger_file_type': 'AddItem'
                        })
                else:
                    invoice['new_item'].append({
                            'item_code': item_code,
                            'description': description,
                            'uom': uom,
                            'rate': 1,
                            'price': unit_price,
                            'unit_uom': 'Unit',
                            'unit_rate': 1,
                            'unit_price': unit_price,
                            'trigger_file_type': 'AddItem'
                        })
            
            if uom == 'Carton':
                invoice['sales_invoice'].append({
                    'invoice_no': invoice_no,
                    'invoice_date': invoice_date,
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'sales_agent': sales_agent,
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'quantity': int(carton_qty),
                    'price': carton_price,
                    'net_amount': net_amount,
                    'discount_amount': discount_amount
                })
            else:
                invoice['sales_invoice'].append({
                    'invoice_no': invoice_no,
                    'invoice_date': invoice_date,
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'sales_agent': sales_agent,
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'quantity': int(unit_qty),
                    'price': unit_price,
                    'net_amount': net_amount,
                    'discount_amount': discount_amount
                })

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)


def process_mp_cn_file(dataframe):
    cn = {'new_item': [], 'cn':[]}
    dataframe = pd.read_excel(dataframe, header=3)
    error = {"error": '', 'message': ''}
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['INV DATE','INV NO','CUST ID','CUSTOMER NAME','PROFILE NAME','SKU NO','SKU DESCRIPTION','UOM','QTY CTN','QTY IN EA','SALES PRICE CTN','SALES PRICE IN EA','TOTAL AMT BEFORE TAX','TOTAL DISC AMT']]

        for index, row in selected_columns.iterrows():
            cn_no = row['INV NO']
            cn_date = row['INV DATE']
            debtor_code = row['CUST ID']
            debtor_name = row['CUSTOMER NAME']
            sales_agent = row['PROFILE NAME']
            item_code = row['SKU NO']
            description = row['SKU DESCRIPTION']
            uom = row['UOM']
            carton_qty = row['QTY CTN']
            carton_price = row['SALES PRICE CTN']
            unit_qty = row['QTY IN EA']
            unit_price = row['SALES PRICE IN EA']
            net_amount = row['TOTAL AMT BEFORE TAX']
            discount_amount = row['TOTAL DISC AMT']

            if pd.isna(sales_agent):
                error['error'] = 'status 404'
                error['message'] = 'check sales agent column'
                return  JsonResponse(error, safe=False, status=status.HTTP_400_BAD_REQUEST)
            item_key = (str(item_code), uom)

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                if uom == 'Carton':
                    cn['new_item'].append({
                            'item_code': item_code,
                            'description': description,
                            'uom': uom,
                            'rate': 1,
                            'price': carton_price,
                            'unit_uom': 'Unit',
                            'unit_rate': 1,
                            'unit_price': 0,
                            'trigger_file_type': 'AddItem'
                        })
                else:
                    cn['new_item'].append({
                            'item_code': item_code,
                            'description': description,
                            'uom': uom,
                            'rate': 1,
                            'price': unit_price,
                            'unit_uom': 'Unit',
                            'unit_rate': 1,
                            'unit_price': unit_price,
                            'trigger_file_type': 'AddItem'
                        })
            
            if uom == 'Carton':
                cn['cn'].append({
                    'cn_no': cn_no,
                    'cn_date': cn_date,
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'sales_agent': sales_agent,
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'quantity': int(carton_qty),
                    'price': carton_price,
                    'net_amount': net_amount,
                    'discount_amount': discount_amount
                })
            else:
                cn['cn'].append({
                    'cn_no': cn_no,
                    'cn_date': cn_date,
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'sales_agent': sales_agent,
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'quantity': abs(int(unit_qty)),
                    'price': unit_price,
                    'net_amount': abs(net_amount),
                    'discount_amount': discount_amount
                })

    return JsonResponse(cn, safe=False, status=status.HTTP_200_OK)
