import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime

def process_dksh_purchase_file(dataframe):
    purchase = {'new_item':[],'purchase':[]}
    user_key_in_uom = []
    dataframe = pd.read_excel(dataframe)
    item_uom_dict = {(item.itemcode, item.uom): item for item in ItemUOM.objects.all() if item.uom == 'CTN'}

    with pd.option_context('display.max_row', None):
        selected_dksh_column = dataframe[['Product code','Product name','Shipment no.','Document date (DKSH)','Closing','Price','Amount']]
        # THERE IS BUGG ON PURCHASING COLUMN
        for index, row in selected_dksh_column.iloc[1:-1].iterrows():
            item_code = row['Product code']
            description = row['Product name']
            delivery_no = row['Shipment no.']
            delivery_date = row['Document date (DKSH)']
            delivered_quatity = row['Closing']
            price = row['Price']
            net_amount = row['Amount']
            
            item_key = (item_code, 'CTN')
            is_item_exist = ItemUOM.objects.filter(itemcode=int(item_code),uom="CTN")
            # print(is_item_exist)
            if not is_item_exist:
                user_key_in_uom.append({
                    'itemcode': int(item_code),
                    'description': description,
                    'delivery_no' : int(delivery_no),
                    'delivery_date': delivery_date,
                    'delivered_quantity': delivered_quatity,
                    'uom': 'CTN',
                    'price': float(price),
                    'rate': 1,
                    'unit_uom': 'UNIT',
                    'unit_price': 0,
                    'unit_rate': 1,
                    'net_amount': net_amount,
                    'exist': 0
                })
            else:
                user_key_in_uom.append({
                    'itemcode': int(item_code),
                    'description': description,
                    'delivery_no' : int(delivery_no),
                    'delivery_date': delivery_date,
                    'delivered_quantity': delivered_quatity,
                    'uom': 'CTN',
                    'price': float(price),
                    'rate': 1,
                    'unit_uom': 'UNIT',
                    'unit_price': 0,
                    'unit_rate': 1,
                    'net_amount': net_amount,
                    'exist': 1
                })
                
    return JsonResponse(user_key_in_uom, safe=False, status=status.HTTP_200_OK)