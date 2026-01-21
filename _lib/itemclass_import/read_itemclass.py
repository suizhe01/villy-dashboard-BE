import pandas as pd
from django.http import JsonResponse
from rest_framework import status

def read_itemclass_file(dataframe):
    itemclass = {'itemclass': []}
    dataframe = pd.read_excel(dataframe)

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['Item Code','Item Class']]

        for index, row in selected_columns.iterrows():
            item_code = row['Item Code']
            item_class = row['Item Class']

            if pd.isna(item_class):
                item_class = ''

            itemclass['itemclass'].append({
                'item_code': item_code,
                'item_class': item_class
            })

    return JsonResponse(itemclass, safe=False, status=status.HTTP_200_OK)


