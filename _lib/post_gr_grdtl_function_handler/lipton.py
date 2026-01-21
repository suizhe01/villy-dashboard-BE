# from branch.models import Branch
# from django.utils import timezone
# from django.db import transaction
# from grdtl.models import GRDTL
# from decimal import Decimal
# from creditor.models import Creditor
# from location.models import Location
# from terms.models import Terms
# from gr.models import GR
# from item.models import Item
# from datetime import datetime

"""
                                            THERE IS NO GR FOR LIPTON
"""

# def create_lipton_gr_grdtl(item_code,document_n_received_date,do_n_invoice_no,received_qty,rate,description,uom,net_amount,price):
#     item_code_instance = Item.objects.filter(itemcode=item_code).first()
#     filter_delivery_no = GR.objects.filter(supplierdono=do_n_invoice_no)
#     date_obj = datetime.strptime(document_n_received_date, "%m/%d/%Y")
#     formatted_date = date_obj.strftime("%Y-%m-%d")
#     document_n_received_date = formatted_date
#     branchautokey = Branch.objects.filter(address__contains = 'Lipton').first()
#     creditor_code_creditor_name = Creditor.objects.filter(companyname='Lipton').first()
#     location_instance = Location.objects.filter(location__contains='Lipton').first()
#     displayterm = Terms.objects.first()
#     current_datetime = timezone.now()

#     if not filter_delivery_no:
#         with transaction.atomic():
#             save_GR = GR(branchautokey=branchautokey,docdate=document_n_received_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierdono=do_n_invoice_no,description='GOODS RECEIVED NOTE',displayterm=displayterm,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,todoctype='PI',lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount, currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4)
#             save_GR.save()

#             totalqty=int(received_qty)*int(rate)
#             get_gr_guid = GR.objects.filter(supplierdono=do_n_invoice_no).first()
#             save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=uom,useruom=uom,qty=received_qty,rate=rate,smallestqty=totalqty,transferedqty=totalqty,unitprice=price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,deliverydate=document_n_received_date,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
#             save_GR_DTL.save()
#     else:
#         #post grdtl
#         # previous_gr_object = get_object_or_404(GR, supplierdono=do_n_invoice_no)
#         previous_gr_object = GR.objects.get(supplierdono = do_n_invoice_no)
#         new_value = previous_gr_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
#         #total,nettotal,localnettotal,analysisnettotal,localanalysisnettotal,totalextax,localtaxableamt,taxcurrencytaxableamt
#         previous_gr_object.total = new_value
#         previous_gr_object.nettotal = new_value
#         previous_gr_object.localnettotal = new_value
#         previous_gr_object.analysisnettotal = new_value
#         previous_gr_object.localanalysisnettotal = new_value
#         previous_gr_object.totalextax = new_value
#         previous_gr_object.localtaxableamt = new_value
#         previous_gr_object.taxcurrencytaxableamt = new_value
#         previous_gr_object.save()

#         totalqty=int(received_qty)*int(rate)
#         get_gr_guid = GR.objects.filter(supplierdono=do_n_invoice_no).first()
#         save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=uom,useruom=uom,qty=received_qty,rate=rate,smallestqty=totalqty,transferedqty=totalqty,unitprice=price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,deliverydate=document_n_received_date,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
#         save_GR_DTL.save()