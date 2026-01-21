import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from itemuom.models import ItemUOM
from datetime import datetime
import re

def process_dob_mamee_invoice_file(dataframe):
    invoice = {'new_item': [], 'sales_invoice':[]}
    dataframe = pd.read_excel(dataframe)
    # dataframe = dataframe.dropna(how='all')
    print(dataframe)
    store_itemcode = []
    item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        # selected_columns = dataframe[['Billing Document','Unnamed: 1','Unnamed: 2','Material','Material.1','Billing Date','Sales Volume Qty','UNIT PRICE','Net Sales Volume']]
        selected_columns = dataframe[['Billing Document','Bill-to Party','Bill-to Party.1','Material','Material.1','Billing Date','Sales Volume Qty','UNIT PRICE','Net Sales Volume']]


        for index, row in selected_columns.iterrows():
            # billing_document = row['Billing Document'].split()
            # sold_to_party = row['Sold-to party'].split(maxsplit=1)
            # material = row['Material'].split(maxsplit=1)

            invoice_no = row['Billing Document']
            invoice_date = str(row['Billing Date'])
            debtor_code = row['Bill-to Party']
            debtor_name = row['Bill-to Party.1']
            item_code = row['Material']
            description = row['Material.1']
            uom = 'CTN'
            quantity = int(row['Sales Volume Qty'])
            price = abs(round(row['UNIT PRICE'],2))
            net_amount = abs(round(row['Net Sales Volume'],2))

            invoice_date = datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S')

            if '(P)' not in description:
                # print(description, '1')
                regex_search = re.search(r'\d+X\d+', description)
                if regex_search:
                    numbers = re.findall(r'\d+', regex_search.group())  
                    numbers = list(map(int, numbers))
                    rate = numbers[0]
                else:
                    # Handle the case with pattern like "8X(4+1)X82G"
                    regex_search = re.search(r'(\d+)X\(\d+\+\d+\)X\d+', description)
                    if regex_search:
                        rate = int(regex_search.group(1))  # Extract the first number (8 in this case)
                # regex_search = re.search(r'\d+X\d+', description)
                # numbers = re.findall(r'\d+', regex_search.group())  
                # numbers = list(map(int, numbers))
                # rate = numbers[0]
            else:
                # print(description, '2')
                regex_search = re.search(r'\d+X\(\d+\+\d+\)', description)
                numbers = re.findall(r'\d+', regex_search.group())  
                numbers = list(map(int, numbers))
                rate = numbers[0]

            item_key = (str(item_code), uom)

            if item_key not in item_uom_dict and item_key not in store_itemcode:
                store_itemcode.append(item_key)
                if '(P)' not in description:
                    regex_search = re.search(r'\d+X\d+', description)
                    numbers = re.findall(r'\d+', regex_search.group())  
                    numbers = list(map(int, numbers))
                    rate = numbers[0]
                    unit_price = round((price/numbers[0]/numbers[1]),2)
                    # print(unit_price)
                    # print(description)
                    # print(test.group())
                else: 
                    regex_search = re.search(r'\d+X\(\d+\+\d+\)', description)
                    numbers = re.findall(r'\d+', regex_search.group())  
                    numbers = list(map(int, numbers))
                    rate = numbers[0]
                    unit_price = round((price/numbers[0]/numbers[1]/numbers[2]),2)

                invoice['new_item'].append({
                            'item_code': item_code,
                            'description': description,
                            'uom': uom,
                            'rate': rate,
                            'price': price,
                            'unit_uom': 'UNT',
                            'unit_rate': 1,
                            'unit_price': unit_price,
                            'trigger_file_type': 'Invoice'
                        })
            
            # print(invoice_date)
            # date_obj = datetime.strptime(invoice_date, "%d/%m/%Y")
            # invoice_date = date_obj.strftime("%Y-%m-%dT00:00:00")
            
            # if pd.isna(invoice_no):
            #     return JsonResponse({"message": "Empty Invoice no"}, safe=False, status=status.HTTP_400_BAD_REQUEST)

            invoice['sales_invoice'].append({
                    'invoice_no': invoice_no,
                    'invoice_date': invoice_date,
                    'debtor_code': debtor_code,
                    'debtor_name': debtor_name,
                    'item_code': item_code,
                    'description': description,
                    'uom': uom,
                    'rate': rate,
                    'quantity': quantity,
                    'price': price,
                    'net_amount': net_amount
                })

    return JsonResponse(invoice, safe=False, status=status.HTTP_200_OK)
