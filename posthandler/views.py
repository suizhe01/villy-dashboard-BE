from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from datetime import datetime
from iv.models import IV
from ivdtl.models import IVDTL
from cn.models import CN
from cndtl.models import CNDTL
from django.db.models import Sum
from item.models import Item
from itemuom.models import ItemUOM
from location.models import Location
from datetime import datetime
from company.models import Company
from branch.models import Branch
from terms.models import Terms
from commissionitemclass.models import CommissionItemClass
from crewrate.models  import CrewRate
from crewratedtl.models import CrewRateDtl
from django.http import FileResponse
import os

# dutchlady function
from _lib.post_pi_pidtl_function_handler.dutchlady import create_dutchlady_pi_pidtl_purchase
from _lib._dutchlady.post_iv_ivdtl_dutchlady import create_dutchlady_iv_ivdtl
from _lib._dutchlady.post_cn_cndtl_dutchlady import create_dutchlady_cn_cndtl
from _lib._dutchlady.post_item_itemuom_function import create_dutchlady_item_itemuom_invoice, create_dutchlady_item_itemuom_cn
from _lib._dutchlady.post_gr_grdtl_dutchlady import create_dutchlady_gr_grdtl

# lipton function
from _lib.post_item_itemuom_function_handler.lipton import create_lipton_item_itemuom_purchase
from _lib.post_pi_pidtl_function_handler.lipton import create_lipton_pi_pidtl
# from _lib.post_iv_ivdtl_function_handler.lipton import create_lipton_iv_ivdtl
# from _lib.post_cn_cndtl_function_handler.lipton import create_lipton_cn_cndtl
from _lib._lipton.post_item_itemuom_function_lipton import create_lipton_item_itemuom_selling,create_lipton_item_itemuom_invoice,create_lipton_item_itemuom_cn
from _lib._lipton.post_iv_ivdtl_lipton import create_lipton_iv_ivdtl
from _lib._lipton.post_cn_cndtl_lipton import create_lipton_cn_cndtl
# from _lib.post_gr_grdtl_function_handler.lipton import create_lipton_gr_grdtl

# DKSH function
from _lib.post_item_itemuom_function_handler.dksh import create_dksh_item_itemuom
from _lib.post_gr_grdtl_function_handler.dksh import create_dksh_gr_grdtl
from _lib._dksh.post_item_itemuom_dksh import create_dksh_item_itemuom_selling, create_dksh_item_itemuom_invoice, create_dksh_item_itemuom_cn
from _lib._dksh.post_iv_ivdtl_dksh import create_dksh_iv_ivdtl
from _lib._dksh.post_cn_cndtl_dksh import create_dksh_cn_cndtl
# mamee function
from _lib.post_item_itemuom_function_handler.mamee import create_mamee_item_itemuom_purchase
from _lib.post_gr_grdtl_function_handler.mamee import create_mamee_gr_grdtl
from _lib.post_pi_pidtl_function_handler.mamee import create_mamee_pi_pidtl
from _lib._mamee.post_iv_ivdtl_mamee import create_mamee_iv_ivdtl
from _lib._mamee.post_item_iteuom_mamee import create_mamee_item_itemuom_invoice,create_mameee_item_itemuom_cn
from _lib._mamee.post_cn_cndtl_mamee import create_mamee_cn_cndtl

# REDBULL function
# from _lib.post_cn_cndtl_function_handler.redbull import create_redbull_cn_cndtl
from _lib._redbull.post_item_itemuom_redbull import create_redbull_item_itemuom_selling, create_redbull_item_itemuom_invoice,create_redbull_item_itemuom_cn
from _lib._redbull.post_iv_vidtl_redbull import create_redbull_iv_ivdtl_invoice
from _lib._redbull.post_cn_cndtl_redbul import create_redbull_cn_cndtl

# COLA function
from _lib.post_item_itemuom_function_handler.cola import create_cola_item_itemuom
from _lib._cola.post_item_itemuom_function_cola import create_cola_item_itemuom_selling,create_cola_item_itemuom_invoice,create_cola_item_itemuom_cn
from _lib._cola.post_iv_ivdtl_cola import create_cola_iv_ivdtl
from _lib._cola.post_cn_cndtl_cola import create_cola_cn_cndtl

from _lib._mp.post_item_itemuom_mp import create_mp_item_iteuom
from _lib._mp.post_iv_ivdtl_mp import create_mp_iv_ivdtl
from _lib._mp.post_cn_cndtl_mp import create_mp_cn_cndtl

from _lib.commission_template.post_commission_template import post_commission_template

from _lib.itemclass_import.update_itemclass import update_item_itemclass

from _lib.commission_add_lorry_crew_transaction.add_lorry_crew_transaction import add_lorry_crew_transaction

################################# DUTCH LADY #################################

def process_in_batches(data, batch_size=300):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

@api_view(['POST'])
def post_dutchlady_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)

        response_list = []
        for batch in process_in_batches(data):
            for item in batch:
                trigger_file_type = item.get('trigger_file_type')
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                # print('test')
                if trigger_file_type == 'CN':
                    create_dutchlady_item_itemuom_cn(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)
                elif trigger_file_type == 'Sell' or trigger_file_type == 'Invoice':
                    create_dutchlady_item_itemuom_invoice(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)

                response_list.append({'item_code': itemcode, 'status': 'success'})
        # return JsonResponse('test',200)
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dutchlady_gr_grdtl_purchase(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for index,item in enumerate(data):
            delivery_no = item.get('good_receive_no')
            delivery_date = item.get('good_receive_date')
            item_code = item.get('item_code')
            batch_no = item.get('batch')
            received_qty = item.get('quantity')
            net_amount = item.get('net_amount')
            uom= item.get('uom')

        #total, nettotal, localnettotal, analysisnettotal, localanalysisnettotal ### sums up of net amount on one DO
            result = create_dutchlady_gr_grdtl(item_code, delivery_date, delivery_no, received_qty, net_amount, batch_no, uom, index)
            if result == "success":
                response_list.append({'delivery_no': delivery_no, 'status': 'success'})
            else:
                response_list.append({'delivery_no': delivery_no, 'status': 'failed', 'reason': result})

    return JsonResponse({'request': 'POST', 'response': response_list, 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dutchlady_pi_pidtl_purchase(request):
    if request.method == 'POST': 
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            delivery_no = item.get('good_receive_no')
            delivery_date = item.get('good_receive_date')
            invoice_no = item.get('purchase_invoice_no')
            invoice_date = item.get('purchase_invoice_date')
            net_amount = item.get('net_amount')
            received_qty = item.get('quantity')
            item_code = item.get('item_code')
            batch_no = item.get('batch_no')
            uom= item.get('uom')
            expiry_date = item.get('product_expiry_date')
            
            result = create_dutchlady_pi_pidtl_purchase(invoice_date,delivery_no,delivery_date,invoice_no,net_amount,received_qty,item_code,batch_no,uom,expiry_date)
            if result == "success":
                response_list.append({'purchase invoice no': invoice_no, 'status': 'success'})
            else:
                response_list.append({'purchase invoice no': invoice_no, 'status': 'failed', 'reason': result})

    return JsonResponse({'request': 'POST', 'response': response_list, 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dutchlady_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first()
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Dutch Lady').first()
        location = Location.objects.filter(location__contains='Dutch Lady').first()
        lorry_driver = 'NA'
        seq = 1
        delete = True
        previous_invoice_no = ''
        udf_book2 = '2'

        response_list = []
        for index,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            invoice_no = item.get('transaction_no')
            invoice_date = item.get('transaction_date')
            description = item.get('description')
            item_code = item.get('item_code')
            box_qty = item.get('box_qty')
            box_rate = item.get('rate')
            box_uom = item.get('uom')
            unit_qty = item.get('unit_qty')
            unit_rate = item.get('unit_rate')
            unit_uom = item.get('unit_uom')
            sales_agent = item.get('sales_agent')
            discount_amt = item.get('discount_amt')
            net_amount = item.get('net_amt')
            box_price = item.get('box_price')
            piece_price = item.get('piece_price')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                seq = 1
                delete = True
                previous_invoice_no = invoice_no
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_dutchlady_iv_ivdtl(debtor_code, debtor_name,invoice_no,invoice_date,item_code,sales_agent,discount_amt,net_amount,box_qty,unit_qty, seq, box_price, piece_price,temporary_display_term,tempcompanyautokey,branchautokey, box_uom,box_rate,unit_uom,unit_rate, location, description, lorry_driver,udf_book2)
            seq += 1
            # response_list.append({'sales invoice no': invoice_no, 'status': 'success'}
    return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dutchlady_cn_cndtl(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first()
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Dutch Lady').first()
        location_instance = Location.objects.filter(location__contains='Dutch Lady').first()
        
        previous_cn_no = ''
        seq = 1
        delete = True
        response_list = []
        for index,item in enumerate(data):
            cn_no = item.get('cn_no')
            cn_date = item.get('cn_date')
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            sales_agent = item.get('sales_man')
            item_code = item.get('item_code')
            description = item.get('description')
            box_qty = item.get('box_qty')
            box_rate = item.get('box_rate')
            box_uom = item.get('box_uom')
            piece_qty = item.get('piece_qty')
            unit_rate = item.get('unit_rate')
            unit_uom = item.get('unit_uom')
            total_amount = item.get('total_amount')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')
            box_price = item.get('box_price')
            unit_price = item.get('unit_price')
            our_invoice_no = item.get('our_invoice_no')

            if previous_cn_no == '':
                previous_cn_no = cn_no
            
            if previous_cn_no != cn_no:
                seq = 1
                delete = True
                previous_cn_no = cn_no
            
            if delete == True:
                filter_header_cn = CN.objects.filter(docno=cn_no).first()
                if filter_header_cn:
                    filter_child_cn = CNDTL.objects.filter(headerautokey=filter_header_cn)
                    if filter_child_cn.exists():
                        filter_child_cn.delete()
                        filter_header_cn.delete()
                        delete = False
                else:
                    delete = False

            create_dutchlady_cn_cndtl(sales_agent,cn_no,  cn_date, debtor_code, debtor_name, item_code, box_qty, piece_qty, total_amount, discount_amount ,net_amount,seq, box_price, unit_price,temporary_display_term,tempcompanyautokey,branchautokey,location_instance,box_rate,box_uom,unit_rate,unit_uom,description,our_invoice_no)
            seq += 1
            # response_list.append({'cn_no': cn_no, 'status': 'success'})
    return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

################################# LIPTON #################################
@api_view(['POST'])
def post_lipton_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        def process_in_batches(data, batch_size=100):
            for i in range(0, len(data), batch_size):
                yield data[i:i + batch_size]
        for batch in process_in_batches(data):
            for item in batch:
                trigger_file_type = item.get('trigger_file_type')
                if trigger_file_type == 'Purchase':
                    itemcode = item.get('item_code')
                    description = item.get('description')
                    uom = item.get('uom')
                    price = item.get('price')
                    rate = item.get('rate')
                    unit_uom = item.get('unit_uom')
                    unit_price = item.get('unit_price')
                    unit_rate = item.get('unit_rate')

                    create_lipton_item_itemuom_purchase(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)
                    response_list.append({'item_code': itemcode, 'status': 'success'})
                elif trigger_file_type =='Sell':
                    itemcode = item.get('item_code')
                    description = item.get('description')
                    uom = item.get('uom')
                    price = item.get('price')
                    rate = item.get('rate')
                    unit_uom = item.get('unit_uom')
                    unit_price = item.get('unit_price')
                    unit_rate = item.get('unit_rate')

                    create_lipton_item_itemuom_selling(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)
                    response_list.append({'item_code': itemcode, 'status': 'success'})
                elif trigger_file_type == 'Invoice':
                    item_code = item.get('item_code')
                    description = item.get('description')
                    uom = item.get('uom')
                    price = item.get('price')
                    rate = item.get('rate')
                    unit_uom = item.get('unit_uom')
                    unit_price = item.get('unit_price')
                    unit_rate = item.get('unit_rate')
                    create_lipton_item_itemuom_invoice(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate)
                    response_list.append({'item_code': item_code, 'status': 'success'})
                elif trigger_file_type =='CN':
                    item_code = item.get('item_code')
                    description = item.get('description')
                    uom = item.get('uom')
                    price = item.get('price')
                    rate = item.get('rate')
                    unit_uom = item.get('unit_uom')
                    unit_price = item.get('unit_price')
                    unit_rate = item.get('unit_rate')
                    create_lipton_item_itemuom_cn(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate)
                    response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'Success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_lipton_pi_pidtl_purchase(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            purchase_invoice_no = item.get('purchase_invoice_no')
            purchase_invoice_date = item.get('purchase_invoice_date')
            net_amount = item.get('net_amount')
            quantity = item.get('quantity')
            item_code = item.get('item_code')
            description = item.get('description')
            uom = item.get('uom')
            product_expiry_date = item.get('product_expiry_date')
            
            create_lipton_pi_pidtl(purchase_invoice_date,product_expiry_date,item_code,purchase_invoice_no,net_amount,quantity,description,uom)
            response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': response_list, 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def post_lipton_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        # delete all child when header is there 

        temporary_display_term = Terms.objects.first()
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Lipton').first()
        location = Location.objects.filter(location='Lipton').first()
        previous_invoice_no = ''
        lorry_driver = 'NA'
        udf_book2 = '2'
        seq = 1
        delete = True
        response_list = []
        for index,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            sales_agent = item.get('sales_agent')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            net_amount = item.get('net_amount')
            discount_amount = item.get('discount_amount')
            quantity = item.get('quantity')
            description = item.get('description')
            item_code = item.get('item_code')
            price= item.get('price')
            uom = item.get('uom')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_lipton_iv_ivdtl(debtor_code, debtor_name,invoice_no,invoice_date,item_code,net_amount, quantity, uom,discount_amount,seq,price,sales_agent,temporary_display_term,tempcompanyautokey,branchautokey,location,description,lorry_driver,udf_book2)
            seq += 1
            # response_list.append({'sales invoice no': invoice_no, 'status': 'success'})
    return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_lipton_cn_cndtl(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first()
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains='Lipton').first()
        location_instance = Location.objects.filter(location__contains='Lipton').first()
        
        previous_cn_no = ''
        delete = True
        seq = 1
        response_list = []
        for index,item in enumerate(data):
            cn_no = item.get('cn_no')
            cn_date = item.get('cn_date')
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            sales_agent = item.get('sales_agent')
            item_code = item.get('item_code')
            description = item.get('description')
            price = item.get('price')
            uom = item.get('uom')
            # rate = item.get('rate')
            quantity = item.get('quantity')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')

            if previous_cn_no == '':
                previous_cn_no = cn_no
            
            if previous_cn_no != cn_no:
                delete = True
                previous_cn_no = cn_no
                seq = 1
            
            if delete == True:
                filter_header_cn = CN.objects.filter(docno=cn_no).first()
                if filter_header_cn:
                    filter_child_cn = CNDTL.objects.filter(headerautokey=filter_header_cn)
                    if filter_child_cn.exists():
                        filter_child_cn.delete()
                        filter_header_cn.delete()
                        delete = False
                else:
                    delete = False
            
            create_lipton_cn_cndtl(sales_agent,cn_no,cn_date,debtor_code,debtor_name,item_code,uom,quantity,discount_amount,net_amount,seq,description,price, temporary_display_term,tempcompanyautokey,branchautokey,location_instance)
            seq += 1
            # response_list.append({'cn no': cn_no, 'status': 'success'})
    return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def post_lipton_gr_grdtl(request):
#     if request.method == 'POST':
#         do_n_invoice_no = request.data.get('document_no')
#         document_n_received_date = request.data.get('received_date')
#         description = request.data.get('description')
#         item_code = request.data.get('itemcode')
#         received_qty = request.data.get('received_qty')
#         net_amount = request.data.get('net_amount')
#         uom = request.data.get('uom')
#         rate = request.data.get('rate')
#         price = request.data.get('price')

#         create_lipton_gr_grdtl(item_code,document_n_received_date,do_n_invoice_no,received_qty,rate,description,uom,net_amount,price)

#         request = {'request':'POST','response':'success', 'status':status.HTTP_201_CREATED}
#     return JsonResponse(request,safe=False, status=status.HTTP_201_CREATED)



################################# MAMEE #################################

@api_view(['POST'])
def post_mamee_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)

        response_list = []
        for item in data:
            trigger_file_type = item.get('trigger_file_type')

            if trigger_file_type == 'Purchase':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                bundle_uom = item.get('bundle_uom')
                bundle_price = item.get('bundle_price')
                bundle_rate = item.get('bundle_rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_mamee_item_itemuom_purchase(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate, bundle_uom, bundle_price, bundle_rate)
                response_list.append({'item_code': itemcode, 'status': 'success'})
            
            elif trigger_file_type == 'Invoice':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                rate = item.get('rate')
                price = item.get('price')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_mamee_item_itemuom_invoice(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)
                response_list.append({'item_code': itemcode, 'status': 'success'})
            
            elif trigger_file_type == 'CN':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_mameee_item_itemuom_cn(item_code,description,uom,price,rate,unit_uom,unit_price,unit_rate)
                response_list.append({'item_code': item_code, 'status': 'success'})

        return JsonResponse({'request': 'POST', 'response': response_list, 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_mamee_gr_grdtl_purchase(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = [] 
        for item in data:
            quantity = item.get('quantity')
            slash_count = quantity.count('/')
            delivery_no = item.get('delivery_no')
            document_date = item.get('transaction_date')
            item_code = item.get('item_code')
            delivery_qty = item.get('quantity')
            net_amount = item.get('net_price')

            create_mamee_gr_grdtl(delivery_no,document_date,item_code,delivery_qty,net_amount, slash_count)
            response_list.append({'Invoice No': item_code, 'status': 'success'})

        return JsonResponse({'request': 'POST', 'response': response_list, 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_mamee_pi_pidtl_purchase(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = [] 
        for item in data:
            quantity = item.get('quantity')
            slash_count = quantity.count('/')
            delivery_no = item.get('delivery_no')
            document_date = item.get('transaction_date')
            item_code = item.get('item_code')
            delivery_qty = item.get('quantity')
            net_amount = item.get('net_price')
            invoice_no = item.get('purchase_invoice_no')

            create_mamee_pi_pidtl(invoice_no, delivery_no,document_date,item_code,delivery_qty,net_amount, slash_count)
            response_list.append({'purchase invoice no': invoice_no, 'status': 'success'})
            
        return JsonResponse({'request': 'POST', 'response': response_list, 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_mamee_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        delete = True
        previous_invoice_no = ''
        seq = 1
        response_list = []
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Mamee').first()
        location = Location.objects.filter(location='Mamee').first()
        temporary_display_term = Terms.objects.first()
        lorry_driver = 'NA'
        udf_book2 = '2'
        for index,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            invoice_no = item.get('invoice_no')
            transaction_date = item.get('invoice_date')
            itemcode = item.get('item_code')
            description = item.get('description')
            salesman = item.get('salesman')
            uom = item.get('uom')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')
            quantity = item.get('quantity')
            price = item.get('price')
            rate = item.get('rate')
            
            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False


            create_mamee_iv_ivdtl(debtor_code,debtor_name,invoice_no,transaction_date,itemcode,salesman,uom,rate,discount_amount,net_amount,quantity, seq,price, tempcompanyautokey, branchautokey, location, description, temporary_display_term,lorry_driver,udf_book2)
            seq += 1
            # response_list.append({'invoice number': invoice_no, 'status': 'success'})

        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_mamee_cn_cndtl(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first() #will be change in future
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Mamee').first()
        location_instance = Location.objects.filter(location__contains='Mamee').first()
        
        delete = True
        previous_cn_no = ''
        seq = 1
        response_list = []
        for index,item in enumerate(data):
            cn_no = item.get('cn_no')
            cn_date = item.get('cn_date')
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            item_code = item.get('item_code')
            description = item.get('description')
            uom = item.get('uom')
            quantity = item.get('quantity')
            sales_agent = item.get('sales_agent')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')

            if previous_cn_no == '':
                previous_cn_no = cn_no
            
            if previous_cn_no != cn_no:
                delete = True
                previous_cn_no = cn_no
                seq = 1
            
            if delete == True:
                filter_header_cn = CN.objects.filter(docno=cn_no).first()
                if filter_header_cn:
                    filter_child_iv = CNDTL.objects.filter(headerautokey=filter_header_cn)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_cn.delete()
                        delete = False
                else:
                    delete = False

            create_mamee_cn_cndtl(cn_no,cn_date,debtor_code,debtor_name,item_code,uom,quantity,sales_agent,discount_amount,net_amount, seq,temporary_display_term,tempcompanyautokey,branchautokey,location_instance, description)
            seq += 1
            # response_list.append({'cn_no': cn_no, 'status': 'success'})

        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

################################# DKSH #################################
@api_view(['POST'])
def post_dksh_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = [] 
        for item in data:
            trigger_file_type = item.get('trigger_file_type')
            if trigger_file_type == 'Sell':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')

                create_dksh_item_itemuom_selling(item_code, description, uom, price, rate)
            elif trigger_file_type == 'Invoice':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_dksh_item_itemuom_invoice(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate)
            elif trigger_file_type == 'CN':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_dksh_item_itemuom_cn(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate)
            
            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dksh_gr_grdtl_purchase(request): 
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = [] 
        for item in data:
            delivery_no = item.get('delivery_no')
            delivery_date = item.get('delivery_date')
            description = item.get('description')
            delivered_quantity = item.get('delivered_quantity')
            item_code = item.get('itemcode')
            net_amount = item.get('net_amount')
            uom = item.get('uom')
            rate = item.get('rate')
            price = item.get('price')

        #total, nettotal, localnettotal, analysisnettotal, localanalysisnettotal ### sums up of net amount on one DO
            
            create_dksh_gr_grdtl(item_code,description, delivery_no,delivery_date,net_amount, delivered_quantity,rate,price,uom)
            response_list.append({'item_code': item_code, 'status': 'success'})
        
        return JsonResponse({'request': 'POST', 'response': response_list, 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dksh_iv_ivdtl_invoice(request): 
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first()
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'DKSH').first()
        location = Location.objects.filter(location='DKSH').first()
        previous_invoice_no = ''
        delete = True
        lorry_driver = 'NA'
        udf_book2 = '2'
        response_list = [] 
        for item in data:
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            customer_name = item.get('customer_name')
            customer_code = item.get('customer_code')
            seq = item.get('seq')
            sales_agent = item.get('sales_agent')
            item_code = item.get('item_code')
            quantity = item.get('quantity')
            description = item.get('description')
            uom = item.get('uom')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False
            
            create_dksh_iv_ivdtl(invoice_no,invoice_date,customer_name,customer_code,seq,sales_agent,item_code,quantity,uom,discount_amount,net_amount,price,description,temporary_display_term,tempcompanyautokey,branchautokey,location,lorry_driver,udf_book2)
            # response_list.append({'item_code': item_code, 'status': 'success'})
        
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dksh_cn_cndtl(request): 
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first() #will be change in future
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'DKSH').first()
        location_instance = Location.objects.filter(location__contains='DKSH').first()
        
        response_list = [] 
        previous_cn_no = ''
        delete =  True
        for item in data:
            cn_no = item.get('cn_no')
            cn_date = item.get('cn_date')
            customer_name = item.get('customer_name')
            customer_code = item.get('customer_code')
            seq = item.get('seq')
            sales_agent = item.get('sales_agent')
            item_code = item.get('item_code')
            description = item.get('description')
            quantity = item.get('quantity')
            uom = item.get('uom')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')

            if previous_cn_no == '':
                previous_cn_no = cn_no
            
            if previous_cn_no != cn_no:
                delete = True
                previous_cn_no = cn_no
                seq = 1
            
            if delete == True:
                filter_header_cn = CN.objects.filter(docno=cn_no).first()
                if filter_header_cn:
                    filter_child_iv = CNDTL.objects.filter(headerautokey=filter_header_cn)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_cn.delete()
                        delete = False
                else:
                    delete = False
            
            create_dksh_cn_cndtl(cn_no,cn_date,customer_name,customer_code,seq,sales_agent,item_code,quantity,uom,discount_amount,net_amount,price,temporary_display_term,tempcompanyautokey,branchautokey,location_instance,description)
            # response_list.append({'item_code': item_code, 'status': 'success'})
        
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)
    
################################# REDBULL #################################
@api_view(['POST'])
def post_redbull_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            trigger_file_type = item.get('trigger_file_type')

            if trigger_file_type == 'Sell':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                rate = item.get('rate')
                price = item.get('price')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_redbull_item_itemuom_selling(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)
                response_list.append({'item_code': itemcode, 'status': 'success'})
            elif trigger_file_type == 'Invoice':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                rate = item.get('rate')
                price = item.get('price')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')
                    
                create_redbull_item_itemuom_invoice(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)
            elif trigger_file_type == 'CN':
                itemcode = item.get('item_code')
                description = item.get('description')
                ctn_uom = item.get('carton_uom')
                ctn_rate = item.get('carton_rate')
                ctn_price = item.get('carton_price')
                otr_uom = item.get('otr_uom')
                otr_rate = item.get('otr_rate')
                otr_price = item.get('otr_price')
                unit_uom = item.get('unit_uom')
                unit_rate = item.get('unit_rate')
                unit_price = item.get('unit_price')

                create_redbull_item_itemuom_cn(itemcode, description, ctn_uom,ctn_rate,ctn_price,otr_uom,otr_rate,otr_price,unit_uom,unit_rate,unit_price)
                response_list.append({'item_code': itemcode, 'status': 'success'})

        return JsonResponse({'request': 'POST', 'response': 'sucess', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_redbull_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Redbull').first()
        location = Location.objects.filter(location='Redbull').first()
        temporary_display_term = Terms.objects.first()
        previous_invoice_no = ''
        seq = 1
        delete = True
        lorry_driver = 'NA'
        udf_book2 = '2'
        response_list = []
        for index,item in enumerate(data):
            debtor_code = item.get('customer_code')
            debtor_name = item.get('customer_name')
            sales_agent = item.get('sales_agent')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            delivery_date = item.get('delivery_date')
            item_code = item.get('item_code')
            description = item.get('description')
            rate = item.get('rate')
            quantity = item.get('quantity')
            uom = item.get('uom')
            total_price = item.get('total_amount')
            discount_amt = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_redbull_iv_ivdtl_invoice(debtor_code, debtor_name,invoice_no,item_code,invoice_date,delivery_date,quantity,total_price,discount_amt,net_amount, uom, seq,price,sales_agent, description, rate, tempcompanyautokey, branchautokey,location, temporary_display_term,lorry_driver,udf_book2)
            seq += 1
            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_redbull_cn_cndtl(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first() #will be change in future
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Redbull').first()
        location_instance = Location.objects.filter(location__contains='Redbull').first()
        
        previous_cn_no = ''
        seq = 1
        delete = True
        response_list = []
        for index,item in enumerate(data):
            cn_no = item.get('cn_no')
            cn_date = item.get('cn_date')
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            sales_agent = item.get('sales_agent')
            invoice_no = item.get('invoice_no')
            net_amount = item.get('net_amount')
            reason_description = item.get('reason_description')
            item_code = item.get('item_code')
            description = item.get('description')
            qty_in_ctn = item.get('qty_in_ctn')
            ctn_rate = item.get('carton_rate')
            ctn_uom = item.get('carton_uom')
            qty_in_otr = item.get('qty_in_otr')
            otr_rate = item.get('otr_rate')
            otr_uom = item.get('otr_uom')
            qty_in_unit = item.get('qty_in_unit')
            unit_rate = item.get('unit_rate')
            unit_uom = item.get('unit_uom')
            ctn_price = item.get('carton_price')
            otr_price = item.get('otr_price')
            unit_price = item.get('unit_price')
            discount_amount = item.get('discount_amount')
            batch_no = item.get('batch_no')

            if previous_cn_no == '':
                previous_cn_no = cn_no
            
            if previous_cn_no != cn_no:
                delete = True
                previous_cn_no = cn_no
                seq = 1
            
            if delete == True:
                filter_header_cn = CN.objects.filter(docno=cn_no).first()
                if filter_header_cn:
                    filter_child_cn = CNDTL.objects.filter(headerautokey=filter_header_cn)
                    if filter_child_cn.exists():
                        filter_child_cn.delete()
                        filter_header_cn.delete()
                        delete = False
                else:
                    delete = False

            create_redbull_cn_cndtl(cn_no,cn_date,debtor_code,debtor_name,invoice_no,net_amount,reason_description,item_code,qty_in_ctn,qty_in_otr,qty_in_unit,discount_amount,batch_no,seq,ctn_price,otr_price,unit_price,temporary_display_term,tempcompanyautokey,branchautokey,location_instance,ctn_rate,ctn_uom,otr_rate,otr_uom,unit_rate,unit_uom,description,sales_agent)
            seq += 1
            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

################################# COLA #################################

@api_view(['POST'])
def post_cola_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            trigger_file_type = item.get('trigger_file_type')
            if trigger_file_type == 'Sell':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')
            
                create_cola_item_itemuom_selling(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate)
            elif trigger_file_type == 'Invoice':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_cola_item_itemuom_invoice(item_code, description,uom,rate,price, unit_uom, unit_price, unit_rate)
            elif trigger_file_type == 'CN':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_cola_item_itemuom_cn(item_code, description,uom,rate,price, unit_uom, unit_price, unit_rate)
        
            response_list.append({'item_code': item_code, 'status': 'success'})
        # print(save_new_item.__dict__)
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_cola_gr_grdtl(request):
    if request.method == 'POST':
        delivery_date = request.data.get('delivery_date')
        po_no = request.data.get('po_no')
        description = request.data.get('description')
        item_code = request.data.get('itemcode')
        delivery_qty = request.data.get('delivery_qty')
        net_amount = request.data.get('net_amount')
        uom= request.data.get('uom')
        rate = request.data.get('rate')
        price = request.data.get('price')

@api_view(['POST'])
def post_cola_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'COLA').first()
        location = Location.objects.filter(location='COLA').first()
        previous_invoice_no = ''
        previous_ewallet_price = ''
        temporary_display_term = Terms.objects.first()
        response_list = []
        del_previous_invoice_no = ''
        delete = True
        lorry_driver='NA'
        udf_book2 = '2'
        for i,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            seq = item.get('seq')
            item_code = item.get('item_code')
            quantity = item.get('quantity')
            uom = item.get('uom')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')
            description = item.get('description')
            price = item.get('price')
            rate = item.get('rate')
            total_invoice_amount = item.get('total_invoice_amount')
            sales_agent = item.get('sales_agent')
            ewallet = item.get('ewallet')

            if del_previous_invoice_no == '':
                del_previous_invoice_no = invoice_no
            
            if del_previous_invoice_no != invoice_no:
                delete = True
                del_previous_invoice_no = invoice_no
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            if ewallet>0:
                total_invoice_amount -= ewallet
            
            create_cola_iv_ivdtl(debtor_code,debtor_name,invoice_no,invoice_date,seq, item_code,quantity,uom, rate,discount_amount,net_amount,total_invoice_amount,price, sales_agent,tempcompanyautokey, branchautokey, location, description, temporary_display_term,lorry_driver,udf_book2)

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
                previous_ewallet_price = ewallet

            if i != (len(data) - 1):
                if invoice_no != previous_invoice_no:
                    main_item = 'T'
                    itemcode_instance = Item.objects.filter(itemcode=item_code).first()
                    description = 'Rounding Adjustment'
                    uom = 'UNIT'
                    rate = 0
                    smallest_qty = 0
                    smallest_unit_price = 0
                    location = Location.objects.filter(location='COLA').first()

                    filter_header_iv = IV.objects.filter(docno=previous_invoice_no).get()

                    if previous_ewallet_price>0:
                        previous_ewallet_price = -previous_ewallet_price
                        filter_ewallet_item = Item.objects.filter(itemcode='PPY').first()
                        filter_ivdtl = IVDTL.objects.filter(headerautokey=filter_header_iv,seq=888)
                        if not filter_ewallet_item:
                            filter_uom = ItemUOM.objects.filter(itemcode='PPY', uom='CTN')
                            filter_unit_uom = ItemUOM.objects.filter(itemcode='PPY', uom='UNIT')
                            mainsupplier = 'COLA'
                            # temcompanyautokey = Company.objects.filter(name='Villy').first()
                            date_time_now = datetime.now()
                            new_item = Item(itembrand='COLA',itemcode='PPY',description='E-WALLET',companyautokey=temcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
                            new_item.save()
                            itemcode_instance = Item.objects.get(itemcode='PPY')
                            if not filter_uom:
                                save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='CTN',rate=1,price=1,lastupdate=0)
                                save_uom.save()
                            if not filter_unit_uom:
                                save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='UNIT',rate=1,price=1,lastupdate=0)
                                save_unit_uom.save()
                        
                        if not filter_ivdtl:
                            itemcode_instance = Item.objects.get(itemcode='PPY')
                            smallest_unit_price = previous_ewallet_price/1
                            new_dtl = IVDTL(seq=888,headerautokey=filter_header_iv,mainitem=main_item,itemcode=itemcode_instance,description='E-WALLET',uom='UNIT',useruom='UNIT',qty=1,rate=1,smallestqty=1,transferedqty=0,smallestunitprice=smallest_unit_price,unitprice=previous_ewallet_price, subtotal=previous_ewallet_price,localsubtotal=previous_ewallet_price,subtotalextax=previous_ewallet_price,location=location,taxableamt=previous_ewallet_price,localsubtotalextax=previous_ewallet_price,localtaxableamt=previous_ewallet_price,taxcurrencytaxableamt=previous_ewallet_price)
                            new_dtl.save()

                    sum_invoice = IVDTL.objects.filter(headerautokey=filter_header_iv).aggregate(total_amount=Sum('subtotal'))
                    rounding_amount = sum_invoice['total_amount'] - filter_header_iv.total
                    filter_rounding = IVDTL.objects.filter(headerautokey=filter_header_iv, seq=999).first()

                    filter_rounding_adjustment_item = Item.objects.filter(itemcode='RD-ADJUST')
                    if not filter_rounding_adjustment_item:
                        filter_unit_uom = ItemUOM.objects.filter(itemcode='RD-ADJUST', uom='UNIT')
                        mainsupplier = 'COLA'
                        # temcompanyautokey = Company.objects.filter(name='Villy').first()
                        date_time_now = datetime.now()
                        new_item = Item(itembrand='COLA',itemcode='RD-ADJUST',description='Rounding Adjustment',companyautokey=temcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
                        new_item.save()
                        itemcode_instance = Item.objects.get(itemcode='RD-ADJUST')
                        if not filter_unit_uom:
                            save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='UNIT',rate=1,price=1,lastupdate=0)
                            save_unit_uom.save()

                    itemcode_instance = Item.objects.get(itemcode='RD-ADJUST')

                    if rounding_amount > 0:
                        if not filter_rounding:
                            create_rounding_positive = IVDTL(seq=999,headerautokey=filter_header_iv,itemcode=itemcode_instance,description=description,uom=uom, useruom=uom,qty=-1,rate=rate, smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=rounding_amount,location=location,transferedqty=0)
                            create_rounding_positive.save()
                        else:
                            filter_existing_rounding = IVDTL.objects.filter(headerautokey=filter_header_iv, seq=999).get()
                            filter_existing_rounding.unitprice = rounding_amount
                            filter_existing_rounding.itemcode = itemcode_instance
                            filter_existing_rounding.qty = -1
                            filter_existing_rounding.save()
                    elif rounding_amount < 0:
                        rounding_amount = abs(rounding_amount)
                        if not filter_rounding:
                            create_rounding_positive = IVDTL(seq=999,headerautokey=filter_header_iv,itemcode=itemcode_instance,description=description,uom=uom, useruom=uom,qty=1,rate=rate, smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=rounding_amount,location=location,transferedqty=0)
                            create_rounding_positive.save()
                        else:
                            filter_existing_rounding = IVDTL.objects.filter(headerautokey=filter_header_iv, seq=999).get()
                            filter_existing_rounding.unitprice = rounding_amount
                            filter_existing_rounding.itemcode = itemcode_instance
                            filter_existing_rounding.qty = 1
                            filter_existing_rounding.save()
                    else:
                        if not filter_rounding:
                            pass
                        else:
                            filter_existing_rounding = IVDTL.objects.filter(headerautokey=filter_header_iv, seq=999).get()
                            filter_existing_rounding.delete()
                    
                    previous_invoice_no = invoice_no
                    previous_ewallet_price = ewallet

            if i == (len(data) - 1):
                main_item = 'T'
                itemcode_instance = Item.objects.filter(itemcode=item_code).first()
                description = 'Rounding Adjustment'
                uom = 'UNIT'
                rate = 0
                smallest_qty = 0
                smallest_unit_price = 0
                location = Location.objects.filter(location='COLA').first()
                
                # seq as 999, quantity -1 or ,1 put at unit price
                filter_header_iv = IV.objects.filter(docno=invoice_no).get()

                if ewallet>0:
                    ewallet = -ewallet
                    filter_ewallet_item = Item.objects.filter(itemcode='PPY')
                    filter_uom = ItemUOM.objects.filter(itemcode='PPY', uom='CTN')
                    filter_unit_uom = ItemUOM.objects.filter(itemcode='PPY', uom='UNIT')
                    filter_ivdtl = IVDTL.objects.filter(headerautokey=filter_header_iv,seq=888)
                    if not filter_ewallet_item:
                        mainsupplier = 'COLA'
                        temcompanyautokey = Company.objects.filter(name='Villy').first()
                        date_time_now = datetime.now()
                        new_item = Item(itembrand='COLA',itemcode='PPY',description='E-WALLET',companyautokey=temcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
                        new_item.save()
                        itemcode_instance = Item.objects.get(itemcode='PPY')
                        if not filter_uom:
                            save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='CTN',rate=1,price=1,lastupdate=0)
                            save_uom.save()
                        if not filter_unit_uom:
                            save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='UNIT',rate=1,price=1,lastupdate=0)
                            save_unit_uom.save()
                    
                    if not filter_ivdtl:
                        itemcode_instance = Item.objects.get(itemcode='PPY')
                        smallest_unit_price = ewallet/1
                        new_dtl = IVDTL(seq=888,headerautokey=filter_header_iv,mainitem=main_item,itemcode=itemcode_instance,description='E-WALLET',uom='UNIT',useruom='UNIT',qty=1,rate=1,smallestqty=1,transferedqty=0,smallestunitprice=smallest_unit_price,unitprice=ewallet, subtotal=ewallet,localsubtotal=ewallet,subtotalextax=ewallet,location=location,taxableamt=ewallet,localsubtotalextax=ewallet,localtaxableamt=ewallet,taxcurrencytaxableamt=ewallet)
                        new_dtl.save()

                sum_invoice = IVDTL.objects.filter(headerautokey=filter_header_iv).aggregate(total_amount=Sum('subtotal'))
                rounding_amount = sum_invoice['total_amount'] - filter_header_iv.total
                filter_rounding = IVDTL.objects.filter(headerautokey=filter_header_iv, seq=999).first()

                itemcode_instance = Item.objects.get(itemcode='RD-ADJUST')

                if rounding_amount > 0:
                    if not filter_rounding:
                        create_rounding_positive = IVDTL(seq=999,headerautokey=filter_header_iv,itemcode=itemcode_instance,description=description,uom=uom, useruom=uom,qty=-1,rate=rate, smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=rounding_amount,location=location,transferedqty=0)
                        create_rounding_positive.save()
                    else:
                        filter_existing_rounding = IVDTL.objects.filter(headerautokey=filter_header_iv, seq=999).get()
                        filter_existing_rounding.unitprice = rounding_amount
                        filter_existing_rounding.itemcode = itemcode_instance
                        filter_existing_rounding.qty = -1
                        filter_existing_rounding.save()
                elif rounding_amount < 0:
                    rounding_amount = abs(rounding_amount)
                    if not filter_rounding:
                        create_rounding_positive = IVDTL(seq=999,headerautokey=filter_header_iv,itemcode=itemcode_instance,description=description,uom=uom, useruom=uom,qty=1,rate=rate, smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=rounding_amount,location=location,transferedqty=0)
                        create_rounding_positive.save()
                    else:
                        filter_existing_rounding = IVDTL.objects.filter(headerautokey=filter_header_iv, seq=999).get()
                        filter_existing_rounding.unitprice = rounding_amount
                        filter_existing_rounding.itemcode = itemcode_instance
                        filter_existing_rounding.qty = 1
                        filter_existing_rounding.save()
                else:
                    if not filter_rounding:
                        pass
                    else:
                        filter_existing_rounding = IVDTL.objects.filter(headerautokey=filter_header_iv, seq=999).get()
                        filter_existing_rounding.delete() 

        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_cola_cn_cndtl(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first() #will be change in future
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'COLA').first()
        location_instance = Location.objects.filter(location__contains='COLA').first()

        previous_cn_no = ''
        previous_ewallet_price = ''
        delete = True
        response_list = []
        del_previous_cn_no = ''
        for i,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            cn_no = item.get('cn_no')
            cn_date = item.get('cn_date')
            seq = item.get('seq')
            item_code = item.get('item_code')
            description = item.get('description')
            quantity = item.get('quantity')
            uom = item.get('uom')
            rate = item.get('rate')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')
            total_invoice_amount = item.get('total_invoice_amount')
            sales_agent = item.get('sales_agent')
            ewallet = item.get('ewallet')
            
            if del_previous_cn_no == '':
                del_previous_cn_no = cn_no
            
            if del_previous_cn_no != cn_no:
                delete = True
                del_previous_cn_no = cn_no
            
            if delete == True:
                filter_header_cn = CN.objects.filter(docno=cn_no).first()
                if filter_header_cn:
                    filter_child_cn = CNDTL.objects.filter(headerautokey=filter_header_cn)
                    if filter_child_cn.exists():
                        filter_child_cn.delete()
                        filter_header_cn.delete()
                        delete = False
                else:
                    delete = False

            if ewallet>0:
                total_invoice_amount = total_invoice_amount - ewallet
            
            create_cola_cn_cndtl(cn_no,cn_date,debtor_code,debtor_name,item_code,uom,rate,quantity,sales_agent,discount_amount,net_amount,seq,total_invoice_amount,temporary_display_term,tempcompanyautokey,branchautokey,location_instance, description)

            if previous_cn_no == '':
                previous_cn_no = cn_no
                previous_ewallet_price = ewallet

            if cn_no != previous_cn_no:
                main_item = 'T'
                itemcode_instance = Item.objects.filter(itemcode=item_code).first()
                description = 'Rounding Adjustment'
                uom = 'UNIT'
                rate = 0
                smallest_qty = 0
                smallest_unit_price = 0
                location = Location.objects.filter(location='COLA').first()

                # seq as 999, quantity -1 or ,1 put at unit price
                filter_header_cn = CN.objects.filter(docno=previous_cn_no).get()

                if previous_ewallet_price>0:
                    previous_ewallet_price = -previous_ewallet_price
                    filter_ewallet_item = Item.objects.filter(itemcode='PPY')
                    filter_cndtl = CNDTL.objects.filter(headerautokey=filter_header_cn,seq=888)
                    if not filter_ewallet_item:
                        filter_uom = ItemUOM.objects.filter(itemcode='PPY', uom='CTN')
                        filter_unit_uom = ItemUOM.objects.filter(itemcode='PPY', uom='UNIT')
                        mainsupplier = 'COLA'
                        temcompanyautokey = Company.objects.filter(name='Villy').first()
                        date_time_now = datetime.now()
                        new_item = Item(itembrand='COLA',itemcode='PPY',description='E-WALLET',companyautokey=temcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
                        new_item.save()
                        itemcode_instance = Item.objects.get(itemcode='PPY')
                        if not filter_uom:
                            save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='CTN',rate=1,price=1,lastupdate=0)
                            save_uom.save()
                        if not filter_unit_uom:
                            save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='UNIT',rate=1,price=1,lastupdate=0)
                            save_unit_uom.save()

                    if not filter_cndtl:
                        itemcode_instance = Item.objects.get(itemcode='PPY')
                        smallest_unit_price = previous_ewallet_price/1
                        new_dtl = CNDTL(headerautokey=filter_header_cn, seq=888,mainitem=main_item,itemcode=itemcode_instance,location=location,description='E-WALLET',uom='UNIT',useruom='UNIT',qty=1,rate=1,smallestqty=1,smallestunitprice=smallest_unit_price,unitprice=previous_ewallet_price,subtotal=previous_ewallet_price,localsubtotal=previous_ewallet_price,printout=0,addtosubtotal='T',iscalcbonuspoint='T',subtotalextax=previous_ewallet_price,goodsreturn='T',taxableamt=previous_ewallet_price,localsubtotalextax=previous_ewallet_price,localtaxableamt=previous_ewallet_price,taxcurrencytaxableamt=previous_ewallet_price)
                        new_dtl.save()

                sum_invoice = CNDTL.objects.filter(headerautokey=filter_header_cn).aggregate(total_amount=Sum('subtotal'))
                rounding_amount = sum_invoice['total_amount'] - filter_header_cn.total
                filter_rounding = CNDTL.objects.filter(headerautokey=filter_header_cn, seq=999).first()
                itemcode_instance = Item.objects.get(itemcode='RD-ADJUST')

                if rounding_amount > 0:
                    rounding_amount = -rounding_amount
                    if not filter_rounding:
                        create_rounding_positive = CNDTL(seq=999,headerautokey=filter_header_cn,itemcode=itemcode_instance,description=description,uom=uom, useruom=uom,qty=1,rate=rate, smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=rounding_amount,location=location)
                        create_rounding_positive.save()
                    else:
                        filter_existing_rounding = CNDTL.objects.filter(headerautokey=filter_header_cn, seq=999).get()
                        filter_existing_rounding.unitprice = rounding_amount
                        filter_existing_rounding.save()
                elif rounding_amount < 0:
                    rounding_amount = abs(rounding_amount)
                    if not filter_rounding:
                        create_rounding_positive = CNDTL(seq=999,headerautokey=filter_header_cn,itemcode=itemcode_instance,description=description,uom=uom, useruom=uom,qty=1,rate=rate, smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=rounding_amount,location=location)
                        create_rounding_positive.save()
                    else:
                        filter_existing_rounding = CNDTL.objects.filter(headerautokey=filter_header_cn, seq=999).get()
                        filter_existing_rounding.unitprice = rounding_amount
                        filter_existing_rounding.save()
                else:
                    if not filter_rounding:
                        pass
                    else:
                        filter_existing_rounding = IVDTL.objects.filter(headerautokey=filter_header_cn, seq=999).get()
                        filter_existing_rounding.delete()
                
                previous_cn_no = cn_no
                previous_ewallet_price = ewallet
                
            
            if i == (len(data) - 1):
                main_item = 'T'
                itemcode_instance = Item.objects.filter(itemcode=item_code).first()
                description = 'Rounding Adjustment'
                uom = 'UNIT'
                rate = 0
                smallest_qty = 0
                smallest_unit_price = 0
                location = Location.objects.filter(location='COLA').first()
                
                # seq as 999, quantity -1 or ,1 put at unit price
                filter_header_cn = CN.objects.filter(docno=cn_no).get()

                if ewallet>0:
                    ewallet = -ewallet
                    filter_ewallet_item = Item.objects.filter(itemcode='PPY')
                    filter_cndtl = CNDTL.objects.filter(headerautokey=filter_header_cn,seq=888)
                    if not filter_ewallet_item:
                        filter_uom = ItemUOM.objects.filter(itemcode='PPY', uom='CTN')
                        filter_unit_uom = ItemUOM.objects.filter(itemcode='PPY', uom='UNIT')
                        mainsupplier = 'COLA'
                        # temcompanyautokey = Company.objects.filter(name='Villy').first()
                        date_time_now = datetime.now()
                        new_item = Item(itembrand='COLA',itemcode='PPY',description='E-WALLET',companyautokey=temcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
                        new_item.save()
                        itemcode_instance = Item.objects.get(itemcode='PPY')
                        if not filter_uom:
                            save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='CTN',rate=1,price=1,lastupdate=0)
                            save_uom.save()
                        if not filter_unit_uom:
                            save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom='UNIT',rate=1,price=1,lastupdate=0)
                            save_unit_uom.save()

                    if not filter_cndtl:
                        itemcode_instance = Item.objects.get(itemcode='PPY')
                        smallest_unit_price = ewallet/1
                        new_dtl = CNDTL(headerautokey=filter_header_cn, seq=888,mainitem=main_item,itemcode=itemcode_instance,location=location,description='E-WALLET',uom='UNIT',useruom='UNIT',qty=1,rate=1,smallestqty=1,smallestunitprice=smallest_unit_price,unitprice=ewallet,subtotal=ewallet,localsubtotal=ewallet,printout=0,addtosubtotal='T',iscalcbonuspoint='T',subtotalextax=ewallet,goodsreturn='T',taxableamt=ewallet,localsubtotalextax=ewallet,localtaxableamt=ewallet,taxcurrencytaxableamt=ewallet)
                        new_dtl.save()

                sum_invoice = CNDTL.objects.filter(headerautokey=filter_header_cn).aggregate(total_amount=Sum('subtotal'))
                rounding_amount = sum_invoice['total_amount'] - filter_header_cn.total
                filter_rounding = CNDTL.objects.filter(headerautokey=filter_header_cn, seq=999).first()
                itemcode_instance = Item.objects.get(itemcode='RD-ADJUST')

                if rounding_amount > 0:
                    rounding_amount = -rounding_amount
                    if not filter_rounding:
                        create_rounding_positive = CNDTL(seq=999,headerautokey=filter_header_cn,itemcode=itemcode_instance,description=description,uom=uom, useruom=uom,qty=1,rate=rate, smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=rounding_amount,location=location)
                        create_rounding_positive.save()
                    else:
                        filter_existing_rounding = CNDTL.objects.filter(headerautokey=filter_header_cn, seq=999).get()
                        filter_existing_rounding.unitprice = rounding_amount
                        filter_existing_rounding.save()
                elif rounding_amount < 0:
                    rounding_amount = abs(rounding_amount)
                    if not filter_rounding:
                        create_rounding_positive = CNDTL(seq=999,headerautokey=filter_header_cn,itemcode=itemcode_instance,description=description,uom=uom, useruom=uom,qty=1,rate=rate, smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=rounding_amount,location=location)
                        create_rounding_positive.save()
                    else:
                        filter_existing_rounding = CNDTL.objects.filter(headerautokey=filter_header_cn, seq=999).get()
                        filter_existing_rounding.unitprice = rounding_amount
                        filter_existing_rounding.save()
                else:
                    if not filter_rounding:
                        pass
                    else:
                        filter_existing_rounding = CNDTL.objects.filter(headerautokey=filter_header_cn, seq=999).get()
                        filter_existing_rounding.delete()

        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)


################################# MAMMY POKO #################################
@api_view(['POST'])
def post_mp_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            trigger_file_type = item.get('trigger_file_type')
            if trigger_file_type == 'AddItem':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')
            
                create_mp_item_iteuom(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate)
        
        # print(save_new_item.__dict__)
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)       

@api_view(['POST'])
def post_mp_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'MAMY POKO').first()
        location = Location.objects.filter(location='MAMY POKO').first()
        temporary_display_term = Terms.objects.first()
        previous_invoice_no = ''
        lorry_driver='NA'
        udf_book2 = '2'
        seq = 1
        delete = True
        response_list = []
        for index,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            sales_agent = item.get('sales_agent')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            item_code = item.get('item_code')
            description = item.get('description')
            uom = item.get('uom')
            quantity = item.get('quantity')
            price = item.get('price')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                seq = 1
                delete = True
                previous_invoice_no = invoice_no
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False
            

            create_mp_iv_ivdtl(debtor_code,debtor_name,sales_agent,invoice_no,invoice_date,item_code,description,uom,quantity,price,discount_amount,net_amount, seq,tempcompanyautokey,branchautokey,location,temporary_display_term,lorry_driver,udf_book2)

            seq += 1

            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_mp_cn_cndtl(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'MAMY POKO').first()
        location = Location.objects.filter(location='MAMY POKO').first()
        temporary_display_term = Terms.objects.first()
        previous_cn_no = ''
        seq = 1
        delete = True
        response_list = []
        for index,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            sales_agent = item.get('sales_agent')
            cn_no = item.get('cn_no')
            cn_date = item.get('cn_date')
            item_code = item.get('item_code')
            description = item.get('description')
            uom = item.get('uom')
            quantity = item.get('quantity')
            price = item.get('price')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')

            if previous_cn_no == '':
                previous_cn_no = cn_no
            
            if previous_cn_no != cn_no:
                seq = 1
                delete = True
                previous_cn_no = cn_no
            
            if delete == True:
                filter_header_cn = CN.objects.filter(docno=cn_no).first()
                if filter_header_cn:
                    filter_child_cn = CNDTL.objects.filter(headerautokey=filter_header_cn)
                    if filter_child_cn.exists():
                        filter_child_cn.delete()
                        filter_header_cn.delete()
                        delete = False
                else:
                    delete = False
            
            create_mp_cn_cndtl(debtor_code,debtor_name,sales_agent,cn_no,cn_date,item_code,description,uom,quantity,price,discount_amount,net_amount, seq,tempcompanyautokey,branchautokey,location,temporary_display_term)

            seq += 1

            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

################################# DOB KARA #################################
from _lib._kara.post_item_itemuom_function import create_kara_item_itemuom_invoice
@api_view(['POST'])
def post_kara_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        for item in data:
            trigger_file_type = item.get('trigger_file_type')
            if trigger_file_type == 'AddItem':
                item_code = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                price = item.get('price')
                rate = item.get('rate')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')
            
                create_kara_item_itemuom_invoice(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate)

        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

from _lib._kara.post_iv_ivdtl_kara import create_kara_iv_ivdtl

@api_view(['POST'])
def post_kara_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        # delete all child when header is there 

        temporary_display_term = Terms.objects.first()
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Kara').first()
        location = Location.objects.filter(location='Kara').first()
        previous_invoice_no = ''
        lorry_driver = 'NA'
        udf_book2 = '2'
        seq = 1
        delete = True
        response_list = []
        for index,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            sales_agent = item.get('sales_agent')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            net_amount = item.get('net_amt')
            discount_amount = item.get('discount_amt')
            quantity = item.get('quantity')
            description = item.get('description')
            item_code = item.get('item_code')
            price= item.get('price')
            rate = item.get('rate')
            uom = item.get('uom')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_kara_iv_ivdtl(debtor_code, debtor_name,invoice_no,invoice_date,item_code,net_amount, quantity, uom,discount_amount,seq,price, rate,sales_agent,temporary_display_term,tempcompanyautokey,branchautokey,location,description,lorry_driver,udf_book2)
            seq += 1
            # response_list.append({'sales invoice no': invoice_no, 'status': 'success'})
    return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

from _lib._kara.post_cn_cndtl_kara import create_kara_cn_cndtl

@api_view(['POST'])
def post_kara_cn_cndtl(request): 
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        temporary_display_term = Terms.objects.first() #will be change in future
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'Kara').first()
        location_instance = Location.objects.filter(location__contains='Kara').first()
        
        response_list = [] 
        previous_cn_no = ''
        delete =  True
        for item in data:
            cn_no = item.get('cn_no')
            cn_date = item.get('cn_date')
            customer_name = item.get('customer_name')
            customer_code = item.get('customer_code')
            seq = item.get('seq')
            sales_agent = item.get('sales_agent')
            item_code = item.get('item_code')
            description = item.get('description')
            quantity = item.get('quantity')
            uom = item.get('uom')
            discount_amount = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')
            reason = item.get('reason')
            our_invoice = item.get('our_invoice')

            if previous_cn_no == '':
                previous_cn_no = cn_no
            
            if previous_cn_no != cn_no:
                delete = True
                previous_cn_no = cn_no
                seq = 1
            
            if delete == True:
                filter_header_cn = CN.objects.filter(docno=cn_no).first()
                if filter_header_cn:
                    filter_child_iv = CNDTL.objects.filter(headerautokey=filter_header_cn)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_cn.delete()
                        delete = False
                else:
                    delete = False
            
            create_kara_cn_cndtl(cn_no,cn_date,customer_name,customer_code,seq,sales_agent,item_code,quantity,uom,discount_amount,net_amount,price,temporary_display_term,tempcompanyautokey,branchautokey,location_instance,description, reason,our_invoice)
            # response_list.append({'item_code': item_code, 'status': 'success'})
        
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)
    

################################# DOB TOHTONKU #################################
from _lib.dob.tohtonku.post_item_itemuom_dob_tohtonku import create_dob_tohtonku_item_iteuom
from _lib.dob.tohtonku.post_iv_ivdtl_dob_tohtonku import create_dob_tohtonku_iv_ivdtl_invoice
@api_view(['POST'])
def post_dob_tohtonku_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            trigger_file_type = item.get('trigger_file_type')

            if trigger_file_type == 'Invoice':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                rate = item.get('rate')
                price = item.get('price')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')
                    
                create_dob_tohtonku_item_iteuom(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)

        return JsonResponse({'request': 'POST', 'response': 'sucess', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def post_dob_tohtonku_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'NA').first()
        location = Location.objects.filter(location='NA').first()
        temporary_display_term = Terms.objects.first()
        previous_invoice_no = ''
        seq = 1
        delete = True
        lorry_driver = 'NA'
        udf_book = '3'
        response_list = []
        sales_agent = 'NA'
        for index,item in enumerate(data):
            debtor_code = item.get('customer_code')
            debtor_name = item.get('customer_name')
            # sales_agent = item.get('sales_agent')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            # delivery_date = item.get('delivery_date')
            item_code = item.get('item_code')
            description = item.get('description')
            rate = item.get('rate')
            quantity = item.get('quantity')
            uom = item.get('uom')
            discount_amt = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_dob_tohtonku_iv_ivdtl_invoice(debtor_code, debtor_name,invoice_no,item_code,invoice_date,quantity,discount_amt,net_amount, uom, seq,price,sales_agent, description, rate, tempcompanyautokey, branchautokey,location, temporary_display_term,lorry_driver,udf_book)
            seq += 1
            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

################################# DOB YLTC #################################
from _lib.dob.yltc.post_item_itemuom_dob_yltc import create_dob_yltc_item_itemuom_invoice
from _lib.dob.yltc.post_iv_ivdtl_dob_yltc import create_dob_yltc_iv_ivdtl_invoice
@api_view(['POST'])
def post_dob_yltc_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            trigger_file_type = item.get('trigger_file_type')

            if trigger_file_type == 'Invoice':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                rate = item.get('rate')
                price = item.get('price')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')
                    
                create_dob_yltc_item_itemuom_invoice(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)

        return JsonResponse({'request': 'POST', 'response': 'sucess', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dob_yltc_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'NA').first()
        location = Location.objects.filter(location='NA').first()
        temporary_display_term = Terms.objects.first()
        previous_invoice_no = ''
        seq = 1
        delete = True
        lorry_driver = 'NA'
        udf_book = '3'
        response_list = []
        sales_agent = 'NA'
        for index,item in enumerate(data):
            debtor_code = item.get('customer_code')
            debtor_name = item.get('customer_name')
            # sales_agent = item.get('sales_agent')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            delivery_date = item.get('delivery_date')
            item_code = item.get('item_code')
            description = item.get('description')
            rate = item.get('rate')
            quantity = item.get('quantity')
            uom = item.get('uom')
            total_price = item.get('total_amount')
            discount_amt = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_dob_yltc_iv_ivdtl_invoice(debtor_code, debtor_name,invoice_no,item_code,invoice_date,delivery_date,quantity,total_price,discount_amt,net_amount, uom, seq,price,sales_agent, description, rate, tempcompanyautokey, branchautokey,location, temporary_display_term,lorry_driver,udf_book)
            seq += 1
            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

################################# DOB SUNQUICK #################################
from _lib.dob.sunquick.post_item_itemuom_dob_sunquick import create_dob_sunquick_item_iteuom
from _lib.dob.sunquick.post_iv_ivdtl_dob_sunquick import create_dob_sunquick_iv_ivdtl_invoice
@api_view(['POST'])
def post_dob_sunquick_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            trigger_file_type = item.get('trigger_file_type')

            if trigger_file_type == 'Invoice':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                rate = item.get('rate')
                price = item.get('price')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')
                    
                create_dob_sunquick_item_iteuom(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)

        return JsonResponse({'request': 'POST', 'response': 'sucess', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def post_dob_sunquick_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'NA').first()
        location = Location.objects.filter(location='NA').first()
        temporary_display_term = Terms.objects.first()
        previous_invoice_no = ''
        seq = 1
        delete = True
        lorry_driver = 'NA'
        udf_book = '3'
        response_list = []
        sales_agent = 'NA'
        for index,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            # sales_agent = item.get('sales_agent')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            item_code = item.get('item_code')
            description = item.get('description')
            # rate = item.get('rate')
            quantity = item.get('quantity')
            uom = item.get('uom')
            discount_amt = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_dob_sunquick_iv_ivdtl_invoice(debtor_code, debtor_name,invoice_no,item_code,invoice_date,quantity,discount_amt,net_amount, uom, seq,price,sales_agent, description, tempcompanyautokey, branchautokey,location, temporary_display_term,lorry_driver,udf_book)
            seq += 1
            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

################################# DOB MAMEE #################################
from _lib.dob.mamee.post_item_itemuom_dob_mamee import create_dob_mamee_item_iteuom
from _lib.dob.mamee.post_iv_ivdtl_dob_mamee import create_dob_mamee_iv_ivdtl_invoice
@api_view(['POST'])
def post_dob_mamee_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_list = []
        for item in data:
            trigger_file_type = item.get('trigger_file_type')

            if trigger_file_type == 'Invoice':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                rate = item.get('rate')
                price = item.get('price')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')
                    
                create_dob_mamee_item_iteuom(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)

        return JsonResponse({'request': 'POST', 'response': 'sucess', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def post_dob_mamee_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains = 'NA').first()
        location = Location.objects.filter(location='NA').first()
        temporary_display_term = Terms.objects.first()
        previous_invoice_no = ''
        seq = 1
        delete = True
        lorry_driver = 'NA'
        udf_book = '3'
        response_list = []
        sales_agent = 'NA'
        for index,item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            item_code = item.get('item_code')
            description = item.get('description')
            rate = item.get('rate')
            quantity = item.get('quantity')
            uom = item.get('uom')
            # discount_amt = item.get('discount_amount')
            net_amount = item.get('net_amount')
            price = item.get('price')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no
            
            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1
            
            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_dob_mamee_iv_ivdtl_invoice(debtor_code, debtor_name,invoice_no,item_code,invoice_date,quantity,rate,net_amount, uom, seq,price,sales_agent, description, tempcompanyautokey, branchautokey,location, temporary_display_term,lorry_driver,udf_book)
            seq += 1
            # response_list.append({'item_code': item_code, 'status': 'success'})
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)


################################# DOB ECOSAFA #################################
from _lib.dob.ecosafa.post_item_itemuom_dob_ecosafa import create_dob_ecosafa_item_iteuom
from _lib.dob.ecosafa.post_iv_ivdtl_dob_ecosafa import create_dob_ecosafa_iv_ivdtl_invoice

@api_view(['POST'])
def post_dob_ecosafa_item_itemuom(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)

        for item in data:
            trigger_file_type = item.get('trigger_file_type')

            if trigger_file_type == 'Invoice':
                itemcode = item.get('item_code')
                description = item.get('description')
                uom = item.get('uom')
                rate = item.get('rate')
                price = item.get('price')
                unit_uom = item.get('unit_uom')
                unit_price = item.get('unit_price')
                unit_rate = item.get('unit_rate')

                create_dob_ecosafa_item_iteuom(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate)

        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def post_dob_ecosafa_iv_ivdtl_invoice(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)

        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        branchautokey = Branch.objects.filter(address__contains='NA').first()
        location = Location.objects.filter(location='NA').first()
        temporary_display_term = Terms.objects.first()
        lorry_driver = 'NA'
        udf_book = '3'
        previous_invoice_no = ''
        seq = 1
        delete = True

        for index, item in enumerate(data):
            debtor_code = item.get('debtor_code')
            debtor_name = item.get('debtor_name')
            invoice_no = item.get('invoice_no')
            invoice_date = item.get('invoice_date')
            item_code = item.get('item_code')
            description = item.get('description')
            rate = item.get('rate')
            quantity = item.get('quantity')
            uom = item.get('uom')

            if previous_invoice_no == '':
                previous_invoice_no = invoice_no

            if previous_invoice_no != invoice_no:
                delete = True
                previous_invoice_no = invoice_no
                seq = 1

            if delete == True:
                filter_header_iv = IV.objects.filter(docno=invoice_no).first()
                if filter_header_iv:
                    filter_child_iv = IVDTL.objects.filter(headerautokey=filter_header_iv)
                    if filter_child_iv.exists():
                        filter_child_iv.delete()
                        filter_header_iv.delete()
                        delete = False
                else:
                    delete = False

            create_dob_ecosafa_iv_ivdtl_invoice(debtor_code, debtor_name, invoice_no, item_code, invoice_date, quantity, rate, uom, seq, tempcompanyautokey, branchautokey, location, temporary_display_term, lorry_driver, udf_book, description)
            seq += 1

        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def post_commission(request):
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        # Upsert mode: no longer deleting all records. post_commission_template handles update-or-create per employee.

        filter_sundry_m = CommissionItemClass.objects.filter(itemclassguid__itemclass="SUNDRY($)").first()
        filter_dob_m = CommissionItemClass.objects.filter(itemclassguid__itemclass="DOB($)").first()
        filter_rb_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="RB(Q)").first()
        filter_yltc_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="YLTC(Q)").first()
        filter_le_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="LE(Q)").first()
        filter_cheers_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="CHEERS(Q)").first()
        filter_rbpallet_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="RB PALLET(Q)").first()
        filter_sajioil_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="SAJIOIL(Q)").first()
        filter_sajioilpallet_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="SAJIOILPALLET(Q)").first()
        filter_sajisweet_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="SAJISWEET(Q)").first()
        filter_sajisweetpallet_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="SAJISWEETPALLET(Q)").first()
        filter_lipton_m = CommissionItemClass.objects.filter(itemclassguid__itemclass="LIPTON($)").first()
        filter_mamee_m = CommissionItemClass.objects.filter(itemclassguid__itemclass="MAMEE($)").first()
        filter_mamypoko_m = CommissionItemClass.objects.filter(itemclassguid__itemclass="MAMYPOKO($)").first()
        filter_dksh_m = CommissionItemClass.objects.filter(itemclassguid__itemclass="DKSH($)").first()
        filter_sunquick_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="SUNQUICK(Q)").first()
        filter_ecosafa_q = CommissionItemClass.objects.filter(itemclassguid__itemclass="ECOSAFA(Q)").first()
        filter_kara_m = CommissionItemClass.objects.filter(itemclassguid__itemclass="KARA($)").first()
        filter_kara_pallet_m = CommissionItemClass.objects.filter(itemclassguid__itemclass="KARA PALLET($)").first()

        for index,item in enumerate(data):
            employee_id = item.get('employee_id')
            crew_name = item.get('crew_name')
            crew_type = item.get('crew_type')
            car_plate = item.get('car_plate')
            sundry_m = item.get('SUNDRY($)')
            dob_m = item.get('DOB($)')
            rb_q = item.get('RB(Q)')
            yltc_q = item.get('YLTC(Q)')
            le_q = item.get('LE(Q)')
            cheers_q = item.get('CHEERS(Q)')
            rbpallet_q = item.get('RBPALLET(Q)')
            sajioil_q = item.get('SAJIOIL(Q)')
            sajioilpallet_q = item.get('SAJIOILPALLET(Q)')
            sajisweet_q = item.get('SAJISWEET(Q)')
            sajisweetpallet_q = item.get('SAJISWEETPALLET(Q)')
            lipton_m = item.get('LIPTON($)')
            mamee_m = item.get('MAMEE($)')
            mamypoko_m = item.get('MAMYPOKO($)')
            dksh_m = item.get('DKSH($)')
            sunquick_q = item.get('SUNQUICK(Q)')
            ecosafa_q = item.get('ECOSAFA(Q)')
            kara_m = item.get('KARA($)')
            kara_pallet_m = item.get('KARAPALLET($)')

            post_commission_template(employee_id,crew_name, crew_type,car_plate, sundry_m,dob_m,rb_q,yltc_q,le_q,cheers_q,rbpallet_q,sajioil_q,sajioilpallet_q,sajisweet_q,sajisweetpallet_q,lipton_m,mamee_m,mamypoko_m,dksh_m,sunquick_q,ecosafa_q,kara_m,kara_pallet_m,filter_sundry_m,filter_dob_m,filter_rb_q,filter_yltc_q,filter_le_q,filter_cheers_q,filter_rbpallet_q,filter_sajioil_q,filter_sajioilpallet_q,filter_sajisweet_q,filter_sajisweetpallet_q,filter_lipton_m,filter_mamee_m,filter_mamypoko_m,filter_dksh_m,filter_sunquick_q,filter_ecosafa_q,filter_kara_m,filter_kara_pallet_m)
        

        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)

class CommissionRatePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def get_employee_commission_details(request):
    crew_name_filter = request.query_params.get('crew_name', None)

    # Fixed display order — any extra classes not in this list are appended at the end
    commission_order = [
        'SUNDRY($)', 'DOB($)', 'LIPTON($)', 'MAMEE($)', 'MAMYPOKO($)', 'DKSH($)',
        'RB(Q)', 'YLTC(Q)', 'LE(Q)', 'CHEERS(Q)', 'RB PALLET(Q)',
        'SAJIOIL(Q)', 'SAJIOILPALLET(Q)', 'SAJISWEET(Q)', 'SAJISWEETPALLET(Q)',
        'SUNQUICK(Q)', 'ECOSAFA(Q)', 'KARA($)', 'KARA PALLET($)',
    ]
    db_item_classes = set(
        CommissionItemClass.objects.select_related('itemclassguid')
        .values_list('itemclassguid__itemclass', flat=True)
    )
    all_item_classes = [c for c in commission_order if c in db_item_classes] + \
                       [c for c in db_item_classes if c not in commission_order]

    crewrates = CrewRate.objects.all().order_by('crewname')
    if crew_name_filter:
        crewrates = crewrates.filter(crewname__icontains=crew_name_filter)

    result = []
    for crewrate in crewrates:
        dtls = CrewRateDtl.objects.filter(
            crewrateguid=crewrate
        ).select_related('commissionitemclassguid__itemclassguid')

        crew_type_map = {}
        for dtl in dtls:
            crew_type = dtl.crewtype
            item_class_name = dtl.commissionitemclassguid.itemclassguid.itemclass
            comm_value = float(dtl.commvalue) if dtl.commvalue else 0

            if '($)' in item_class_name:
                comm_value = round(comm_value * 100, 4)

            if crew_type not in crew_type_map:
                crew_type_map[crew_type] = {
                    'employee_id': crewrate.crewid,
                    'crew_name': crewrate.crewname,
                    'crew_type': crew_type,
                }
            crew_type_map[crew_type][item_class_name] = comm_value

        result.extend(crew_type_map.values())

    paginator = CommissionRatePagination()
    page = paginator.paginate_queryset(result, request)

    fixed_headers = ['employee_id', 'crew_name', 'crew_type']
    headers = fixed_headers + all_item_classes

    return Response({
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'headers': headers,
        'rows': page,
    })

@api_view(['POST'])
def commission_add_lorry_crew_transaction(request):
    if request.method == 'POST':
        data = request.data
        # if not isinstance(data, list):
        #     return JsonResponse({'error': 'Invalid data format. Expected a list of JSON objects.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        lorry_guid = data.get('lorry_guid')
        doc_no = data.get('doc_no')

        response = add_lorry_crew_transaction(lorry_guid, doc_no, tempcompanyautokey)
        if response is None:
            pass
        else:
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return response  # Return the 404 response immediately
            elif response.status_code == status.HTTP_409_CONFLICT:
                return response
            elif response.status_code == status.HTTP_201_CREATED:
                return response
        
        # print(add_lorry_crew_transaction(lorry_guid,doc_no,tempcompanyautokey))
        
        return JsonResponse({'request': 'POST', 'response': 'success', 'status': status.HTTP_201_CREATED}, safe=False, status=status.HTTP_201_CREATED)
    
from _lib.calculate_commission_by_date.calculate_commission import calculate_commission_by_date

@api_view(['POST'])
def calculate_commission(request):
    if request.method == 'POST':
        data = request.data
        
        tempcompanyautokey = Company.objects.filter(name='Villy').first()

        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d").date()
        # end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d").date()
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")  
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999000)  # Add time component

        response = calculate_commission_by_date(start_date, end_date,tempcompanyautokey)
        
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)

from _lib.calculate_commission_by_date.get_commission_by_crewid import display_calculated_comm_by_crewid

@api_view(['POST'])
def display_commission_by_crew_id(request):
    if request.method == 'POST':
        data = request.data

        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d").date()
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")  
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999000)  # Add time component
        crew_id = data.get('crew_id')

        response = display_calculated_comm_by_crewid(start_date, end_date, crew_id)

        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
    
from _lib.calculate_commission_by_date.get_commission_by_crewdtlguid import display_calculated_comm_by_crewguid
@api_view(['POST'])
def display_commission_by_crew_guid(request):
    if request.method == 'POST':
        data = request.data

        crew_guid = data.get('crew_guid')

        response = display_calculated_comm_by_crewguid(crew_guid)

        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)

from _lib.calculate_commission_by_date.get_transaction_by_lorryguid import display_calculated_comm_by_lorryguid
@api_view(['POST'])
def display_commission_by_lorry_guid(request):
    if request.method == 'POST':
        data = request.data

        lorry_guid = data.get('lorry_guid')

        response = display_calculated_comm_by_lorryguid(lorry_guid)

        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)



from _lib.custom_get.get_crew import get_crew_details
@api_view(['GET'])
def custom_get_crew(request):
    if request.method == 'GET':
        # data = request.data
        response = get_crew_details()
        if response is None:
            return JsonResponse({"error": "No crew details found"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)

from _lib.custom_create.create_crew import create_crew
from lorry.models import Lorry
@api_view(['POST'])
def custom_create_crew(request):
    if request.method == 'POST':
        data = request.data
        
        lorry_guid = data.get('lorryguid')
        crew_id = data.get('crewid')
        crew_type = data.get('crewtype')

        lorry_guid = Lorry.objects.get(lorryguid=lorry_guid)
        response = create_crew(lorry_guid,crew_id,crew_type)
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)

from _lib.custom_delete.delete_crew import delete_crew

@api_view(['POST'])
def custom_delete_crew(request):
    if request.method == 'POST':
        data = request.data
        
        lorry_guid = data.get('lorryguid')
        crew_id = data.get('crewid')

        lorry_guid = Lorry.objects.get(lorryguid=lorry_guid)
        response = delete_crew(lorry_guid,crew_id)
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
    
from _lib.custom_delete.delete_transaction import delete_transaction
@api_view(['POST'])
def custom_delete_transaction(request):
    if request.method == 'POST':
        data = request.data
        
        lorry_guid = data.get('lorryguid')
        doc_no = data.get('docno')

        lorry_guid = Lorry.objects.get(lorryguid=lorry_guid)
        response = delete_transaction(lorry_guid,doc_no)
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
    
# UPDATE LORRY NUMBER AND TRANSACTION DATE
from _lib.custom_update.update_lorry import update_lorry_number
@api_view(['POST'])
def custom_update_lorry_plate(request):
    if request.method == 'POST':
        data = request.data

        lorry_guid = data.get('lorry_guid')
        lorry_number = data.get('lorry_number')
        date = data.get('date')

        lorry_guid = Lorry.objects.get(lorryguid=lorry_guid)
        response = update_lorry_number(lorry_guid, lorry_number, date)
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

from _lib.calculate_commission_by_date.export_report import export_report_by_date
@api_view(['POST'])
def export_crew(request):
    if request.method == 'POST':
        data = request.data
        
        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d").date()
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")  
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999000)  # Add time component

        file_path = export_report_by_date(start_date, end_date)

        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_path),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # Delete the file after response is ready
        os.remove(file_path)

        return response

from _lib.search_transaction.search_invoice import search_invoice
@api_view(['POST'])
def search_transaction(request):
    if request.method == 'POST':
        data = request.data

        invoice = data.get('invoice_no')
        response = search_invoice(invoice)

        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
    

from _lib.commission_report.commission_list_report import list_report
@api_view(['POST'])
def print_commission_list_report(request):
    if request.method == 'POST':
        data = request.data

        lorry_number = data.get("lorry_number")
        document_date = data.get("document_date")
        employee_details = data.get("employee_details")
        invoice_list_no = data.get("invoice_list")
        generator_name = data.get("generator_name")

        return list_report(lorry_number, document_date, employee_details, invoice_list_no, generator_name)

        # list_report(lorry_number, document_date, employee_details, invoice_list_no)
        # # response = 

        # return JsonResponse("response", safe=False, status=status.HTTP_200_OK)



