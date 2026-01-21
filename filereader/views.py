from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import pandas as pd
import os
from .serializers import FileUploadSerializer
from rest_framework import viewsets

from _lib.process_imported_file_function_handler.dutchlady import process_dutchlady_purchase_file
from _lib.process_imported_file_function_handler.lipton import process_lipton_purchase_file
from _lib.process_imported_file_function_handler.dksh import process_dksh_purchase_file
# from _lib.process_imported_file_function_handler.cola import process_cola_file
from _lib.process_imported_file_function_handler.mamee import process_mamee_purchase_file
from _lib._dutchlady.read_item_itemuom_dutchlady import get_dutchlady_item_itemuom_sell,process_dutchlady_invoice_file, process_dutchlady_cn_file
from _lib._lipton.read_item_itemuom_lipton import get_lipton_item_itemuom_sell, process_lipton_invoice_file, process_lipton_cn_file
from _lib._cola.read_item_itemuom_cola import get_cola_item_itemuom_sell, process_cola_invoice_file,process_cola_cn_file
from _lib._redbull.read_item_itemuom_redbull import get_redbull_item_itemuom_sell, process_redbull_invoice_file, process_redbull_cn_file
from _lib._dksh.read_item_itemuom_dksh import get_dksh_item_itemuom_sell, get_dksh_invoice_file,get_dksh_cn_file
from _lib._mamee.read_item_itemuom_mamee import process_mamee_invoice_file, process_mamee_cn_file
from _lib._mp.read_item_itemuom_mp import process_mp_itemcode_file, process_mp_invoice_file, process_mp_cn_file
from _lib.commission_template.read_commission import process_commission_file
from _lib.itemclass_import.read_itemclass import read_itemclass_file
from _lib.dob.yltc.read_yltc import process_dob_yltc_invoice_file
from _lib.dob.sunquick.read_sunquick import process_dob_sunquick_invoice_file
from _lib.dob.mamee.read_mamee import process_dob_mamee_invoice_file
from _lib.dob.tohtonku.read_tohtonku import process_dob_tohtonku_invoice_file
from _lib._kara.read_item_itemuom_kara import process_kara_invoice_file, process_kara_cn_file

def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()

@api_view(['POST'])
def upload_and_process_excel(request):
    """
    body
    """
    if request.method == 'POST':
        uploaded_file_to_str = str(request.data.get('file'))
        uploaded_file = request.data.get('file')
        if uploaded_file is not None:
            # Read the Excel file using pandas
            try:
                if get_file_type(uploaded_file_to_str) == '.csv':
                    # dataframe = pd.read_csv(uploaded_file)
                    # convertdataframetolist = dataframe.columns.tolist()
                    file_name = str(uploaded_file).split(' ')[0].upper()
                    if file_name == 'LIPTON-PURCHASE':
                        return process_lipton_purchase_file(uploaded_file)          # PROCESS LIPTON PURCHASE FILE
                    elif file_name == 'LIPTON-INVOICE':
                        return process_lipton_invoice_file(uploaded_file)           # PROCESS LIPTON INVOICE FILE
                    elif file_name == 'LIPTON-CN':
                        return process_lipton_cn_file(uploaded_file)           # PROCESS LIPTON CN FILE
                elif get_file_type(uploaded_file_to_str) == '.xlsx':
                    dataframe = pd.read_excel(uploaded_file)
                    # print(dataframe)
                    # print(uploaded_file)
                    file_name = str(uploaded_file).split(' ')[0].upper()
                    print(file_name)
                    if file_name == 'DUTCHLADY-PURCHASE':
                        return process_dutchlady_purchase_file(uploaded_file)       # PROCESS DUTCHLADY PURCHASE FILE
                    elif file_name == 'COLA-INVOICE':
                        return process_cola_invoice_file(uploaded_file)             #PROCESS COLA INVOICE FILE
                    elif file_name == 'COLA-CN':
                        return process_cola_cn_file(uploaded_file)                  #PROCESS COLA CN FILE
                    elif file_name == 'MAMEE-CN':
                        return process_mamee_cn_file(uploaded_file)                 # PROCESS MAMEE CN FILE
                    elif file_name == 'DUTCHLADY-CN':
                        return process_dutchlady_cn_file(uploaded_file)             # PROCESS DUTCHLADY CN FILE
                    elif file_name == 'DUTCHLADY-INVOICE':
                        return process_dutchlady_invoice_file(uploaded_file)        # PROCESS DUTCHLADY INVOICE FILE
                    elif file_name == 'MAMEE-PURCHASE':
                        return process_mamee_purchase_file(uploaded_file)           # PROCESS MAMEE PURCHASE FILE
                    elif file_name == 'MAMEE-INVOICE':
                        return process_mamee_invoice_file(uploaded_file)            # PROCESS MAMEE INVOICE FILE
                    elif file_name == 'DKSH-CN':
                        return get_dksh_cn_file(uploaded_file)                      # PROCESS DKSH CN FILE
                    elif file_name == 'MP-ITEMCODE':
                        return process_mp_itemcode_file(uploaded_file)              # PROCESS MP ITEM FILE
                    elif file_name == 'MP-INVOICE':
                        return process_mp_invoice_file(uploaded_file)               # PROCESS INVOICE FILE
                    elif file_name == 'MP-CN':
                        return process_mp_cn_file(uploaded_file)
                    elif file_name == 'COMMISSION-RATE':
                        return process_commission_file(uploaded_file)
                    elif file_name == 'IMPORT_ITEMCLASS':
                        return read_itemclass_file(uploaded_file)
                    elif file_name == 'DOB_SUNQUICK-INVOICE':
                        return process_dob_sunquick_invoice_file(uploaded_file)
                    elif file_name == 'DOB_MAMEE-INVOICE':
                        return process_dob_mamee_invoice_file(uploaded_file)
                    elif file_name == 'DOB_YLTC-INVOICE':
                        return process_dob_yltc_invoice_file(uploaded_file) 
                    elif file_name == 'REDBULL-CN':
                        return process_redbull_cn_file(uploaded_file) 
                    elif file_name == 'DOB_TOHTONKU-INVOICE':
                        return process_dob_tohtonku_invoice_file(uploaded_file)
                    elif file_name == 'REDBULL-INVOICE':
                        return process_redbull_invoice_file(uploaded_file)      #PROCESS REBULL INVOICE FILE
                    elif file_name == 'KARA-INVOICE':
                        return process_kara_invoice_file(uploaded_file)  
                    elif file_name == 'KARA-CN':
                        return process_kara_cn_file(uploaded_file)
                elif get_file_type(uploaded_file_to_str) == '.xls':
                    dataframe = pd.read_excel(uploaded_file)
                    convertdataframetolist = dataframe.columns.tolist()
                    file_name = str(uploaded_file).split(' ')[0].upper()
                    print(file_name)
                    # print(convertdataframetolist)
                    
                    if file_name == 'DKSH-INVOICE':
                        return get_dksh_invoice_file(uploaded_file)
                    elif file_name == 'REDBULL-INVOICE':
                        return process_redbull_invoice_file(uploaded_file)      #PROCESS REBULL INVOICE FILE
                    elif file_name == 'REDBULL-CN':
                        return process_redbull_cn_file(uploaded_file)           #PROCESS REBULL CN FILE
                    elif file_name == 'DKSH-PURCHASE':
                        return process_dksh_purchase_file(uploaded_file)        #PROCESS DKSH PURCHASE FILE
                    elif file_name == 'DUTCHLADY-ITEMCODE':
                        return get_dutchlady_item_itemuom_sell(uploaded_file)   # PROCESS DUTCHLADY SELLING PRICE
                    elif file_name == 'LIPTON-ITEMCODE':
                        return get_lipton_item_itemuom_sell(uploaded_file)      
                    elif file_name == 'COLA-ITEMCODE':
                        return get_cola_item_itemuom_sell(uploaded_file)        
                    elif file_name == 'REDBULL-ITEMCODE':
                        return get_redbull_item_itemuom_sell(uploaded_file)     
                    elif file_name == 'DKSH-ITEMCODE':
                        return get_dksh_item_itemuom_sell(uploaded_file)    
                    elif file_name == 'DOB_YLTC-INVOICE':
                        return process_dob_yltc_invoice_file(uploaded_file)    
                return Response({'error': 'Wong file name','message': 'Please upload a file with the correct name format.'}, status=status.HTTP_400_BAD_REQUEST)
            except pd.errors.ParserError as e:
                return Response({'error': 'Invalid Excel file format'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)


