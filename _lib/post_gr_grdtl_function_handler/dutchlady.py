# from django.db import transaction
# from grdtl.models import GRDTL
# from decimal import Decimal
# from creditor.models import Creditor
# from branch.models import Branch
# from location.models import Location
# from gr.models import GR
# from terms.models import Terms
# from item.models import Item
# from _lib.panda import current_date_time
# from itemuom.models import ItemUOM
# from django.core.exceptions import ObjectDoesNotExist

# def create_dutchlady_gr_grdtl(item_code,delivery_date,delivery_no,received_qty,net_amount,batch_no,uom, seq):
#     item_code_instance = Item.objects.filter(itemcode=item_code).first()
#     filter_delivery_no = GR.objects.filter(supplierdono=delivery_no)
#     branchautokey = Branch.objects.filter(address__contains = 'Dutch Lady').first()
#     creditor_code_creditor_name = Creditor.objects.filter(companyname='Dutch Lady').first()
#     location_instance = Location.objects.filter(location__contains='Dutch Lady').first()
#     displayterm = Terms.objects.first()
#     current_datetime = current_date_time()
#     try:
#         get_uom_object = ItemUOM.objects.get(itemcode=item_code, uom=uom)
#     except ObjectDoesNotExist:
#         return f"UOM or item code does not exist."
#     get_item_object = Item.objects.get(itemcode=item_code)
#     rate = get_uom_object.rate
#     price = get_uom_object.price
#     description = get_item_object.description

#     if not filter_delivery_no:
#         with transaction.atomic():
#             save_GR = GR(branchautokey=branchautokey,docdate=delivery_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierdono=delivery_no,description='GOODS RECEIVED NOTE',displayterm=displayterm,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,todoctype='PI',lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount, currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4)
#             save_GR.save()

#             get_gr_guid = GR.objects.filter(supplierdono=delivery_no).first()
#             smallest_qty_box = received_qty*int(rate)
#             smallest_unit_price_box = price/rate
#             # box_total_amount = received_qty * price
#             save_GR_DTL = GRDTL(seq=seq,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,batchno=batch_no,description=description,uom=uom,useruom=uom,qty=received_qty,rate=rate,smallestqty=smallest_qty_box,transferedqty=smallest_qty_box,smallestunitprice=smallest_unit_price_box,unitprice=price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,deliverydate=delivery_date,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
#             save_GR_DTL.save()
#     else:
#         get_gr_object = GR.objects.get(supplierdono=delivery_no)
#         filter_gr_grdtl = GRDTL.objects.filter(itemcode=item_code,batchno=batch_no, grautokey=get_gr_object)
#         smallest_qty_box = received_qty*int(rate)
#         smallest_unit_price_box = price/rate
#         get_gr_guid = GR.objects.filter(supplierdono=delivery_no).first()
#         # box_total_amount = received_qty * price

#         if not filter_gr_grdtl:
#             new_gr_dtl = GRDTL(seq=seq,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,batchno=batch_no,description=description,uom=uom,useruom=uom,qty=received_qty,rate=rate,smallestqty=smallest_qty_box,transferedqty=smallest_qty_box,smallestunitprice=smallest_unit_price_box,unitprice=price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,deliverydate=delivery_date,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
#             new_gr_dtl.save()
                
#             new_value = get_gr_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
#             get_gr_object.total = new_value
#             get_gr_object.nettotal = new_value
#             get_gr_object.localnettotal = new_value
#             get_gr_object.analysisnettotal = new_value
#             get_gr_object.localanalysisnettotal = new_value
#             get_gr_object.totalextax = new_value
#             get_gr_object.localtaxableamt = new_value
#             get_gr_object.taxcurrencytaxableamt = new_value
#             get_gr_object.save()
#         else:
#             get_gr_amount = GR.objects.get(supplierdono=delivery_no).total
#             filter_gr_grdtl_object = GRDTL.objects.get(itemcode=item_code,batchno=batch_no, grautokey=get_gr_object)
#             previous_net_amount = filter_gr_grdtl_object.subtotal
#             get_gr_amount = get_gr_amount - previous_net_amount + Decimal(net_amount).quantize(Decimal('0.00'))
            
#             filter_gr_grdtl_object.qty = net_amount
#             filter_gr_grdtl_object.subtotal = net_amount
#             filter_gr_grdtl_object.localsubtotal = net_amount
#             filter_gr_grdtl_object.subtotalextax = net_amount
#             filter_gr_grdtl_object.taxableamt = net_amount
#             filter_gr_grdtl_object.localsubtotalextax = net_amount
#             filter_gr_grdtl_object.localtaxableamt = net_amount
#             filter_gr_grdtl_object.taxcurrencytaxableamt = net_amount
#             filter_gr_grdtl_object.smallestqty = smallest_qty_box
#             filter_gr_grdtl_object.smallestunitprice = smallest_unit_price_box
#             filter_gr_grdtl_object.qty = received_qty
#             filter_gr_grdtl_object.save()
            
#             get_gr_object.total = get_gr_amount
#             get_gr_object.nettotal = get_gr_amount
#             get_gr_object.localnettotal = get_gr_amount
#             get_gr_object.analysisnettotal = get_gr_amount
#             get_gr_object.localanalysisnettotal = get_gr_amount
#             get_gr_object.totalextax = get_gr_amount
#             get_gr_object.localtaxableamt = get_gr_amount
#             get_gr_object.taxcurrencytaxableamt = get_gr_amount
#             get_gr_object.save()
            

#         # #post grdtl
#         # # previous_gr_object = get_object_or_404(GR, supplierdono=delivery_no)
#         # previous_gr_object = GR.objects.get(supplierdono = delivery_no)
#         # new_value = previous_gr_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
#         # #total,nettotal,localnettotal,analysisnettotal,localanalysisnettotal,totalextax,localtaxableamt,taxcurrencytaxableamt
#         # previous_gr_object.total = new_value
#         # previous_gr_object.nettotal = new_value
#         # previous_gr_object.localnettotal = new_value
#         # previous_gr_object.analysisnettotal = new_value
#         # previous_gr_object.localanalysisnettotal = new_value
#         # previous_gr_object.totalextax = new_value
#         # previous_gr_object.localtaxableamt = new_value
#         # previous_gr_object.taxcurrencytaxableamt = new_value
#         # previous_gr_object.save()

#         # get_gr_guid = GR.objects.filter(supplierdono=delivery_no).first()
#         # smallest_qty_box = received_qty*int(rate)
#         # smallest_unit_price_box = price/rate
#         # box_total_amount = received_qty * price
#         # save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,batchno=batch_no,description=description,uom=uom,useruom=uom,qty=received_qty,rate=rate,smallestqty=smallest_qty_box,transferedqty=smallest_qty_box,smallestunitprice=smallest_unit_price_box,unitprice=price,subtotal=box_total_amount,localsubtotal=box_total_amount,subtotalextax=box_total_amount,deliverydate=delivery_date,taxableamt=box_total_amount,localsubtotalextax=box_total_amount,localtaxableamt=box_total_amount,taxcurrencytaxableamt=box_total_amount)
#         # save_GR_DTL.save()

#     return "success"