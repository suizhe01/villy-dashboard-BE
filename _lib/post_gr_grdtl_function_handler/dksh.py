from django.db import transaction
from grdtl.models import GRDTL
from decimal import Decimal
from creditor.models import Creditor
from branch.models import Branch
from location.models import Location
from gr.models import GR
from terms.models import Terms
from item.models import Item
from _lib.panda import current_date_time

def create_dksh_gr_grdtl(item_code,description, delivery_no,delivery_date,net_amount, delivered_quantity,rate,price,uom):
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    filter_delivery_no = GR.objects.filter(supplierdono=delivery_no)
    branchautokey = Branch.objects.filter(address__contains = 'DKSH').first()
    creditor_code_creditor_name = Creditor.objects.filter(companyname='DKSH').first()
    location_instance = Location.objects.filter(location__contains='DKSH').first()
    displayterm = Terms.objects.first()
    current_datetime = current_date_time()

    if not filter_delivery_no:
        with transaction.atomic():
            save_GR = GR(branchautokey=branchautokey,docdate=delivery_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierdono=delivery_no,description='GOODS RECEIVED NOTE',displayterm=displayterm,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,todoctype='PI',lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount, currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4)
            save_GR.save()

            get_gr_guid = GR.objects.filter(supplierdono=delivery_no).first()
            smallest_qty = delivered_quantity * int(rate)
            smallest_unit_price = price/rate
            total_amount = delivered_quantity * price
            save_GRDTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=uom,useruom=uom,qty=delivered_quantity,rate=rate,smallestqty=smallest_qty,transferedqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=price,subtotal=total_amount,localsubtotal=total_amount,subtotalextax=total_amount,deliverydate=delivery_date,taxableamt=total_amount,localsubtotalextax=total_amount,localtaxableamt=total_amount,taxcurrencytaxableamt=total_amount)
            save_GRDTL.save()
    else:
        #post grdtl
        previous_gr_object = GR.objects.get(supplierdono = delivery_no)
        new_value = previous_gr_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
        #total,nettotal,localnettotal,analysisnettotal,localanalysisnettotal,totalextax,localtaxableamt,taxcurrencytaxableamt
        previous_gr_object.total = new_value
        previous_gr_object.nettotal = new_value
        previous_gr_object.localnettotal = new_value
        previous_gr_object.analysisnettotal = new_value
        previous_gr_object.localanalysisnettotal = new_value
        previous_gr_object.totalextax = new_value
        previous_gr_object.localtaxableamt = new_value
        previous_gr_object.taxcurrencytaxableamt = new_value
        previous_gr_object.lastmodified = current_datetime
        previous_gr_object.save()

        get_gr_guid = GR.objects.filter(supplierdono=delivery_no).first()
        smallest_qty = delivered_quantity * int(rate)
        smallest_unit_price = price/rate
        total_amount = delivered_quantity * price
        save_GRDTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=uom,useruom=uom,qty=delivered_quantity,rate=rate,smallestqty=smallest_qty,transferedqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=price,subtotal=total_amount,localsubtotal=total_amount,subtotalextax=total_amount,deliverydate=delivery_date,taxableamt=total_amount,localsubtotalextax=total_amount,localtaxableamt=total_amount,taxcurrencytaxableamt=total_amount)
        save_GRDTL.save()
    
