from django.utils import timezone
from django.db import transaction
from grdtl.models import GRDTL
from decimal import Decimal
from creditor.models import Creditor
from branch.models import Branch
from location.models import Location
from gr.models import GR
from terms.models import Terms
from item.models import Item
from _lib.panda import convert_date_from_dd_mm_yyyy
from itemuom.models import ItemUOM

def create_mamee_gr_grdtl(delivery_no,document_date,item_code,delivery_qty,net_amount, slash_count):
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    filter_delivery_no = GR.objects.filter(supplierdono=delivery_no)
    branchautokey = Branch.objects.filter(address = 'Mamee').first()
    creditor_code_creditor_name = Creditor.objects.filter(companyname='Mamee').first()
    location_instance = Location.objects.filter(location='Mamee').first()
    displayterm = Terms.objects.first()
    current_datetime = timezone.now()
    document_date = convert_date_from_dd_mm_yyyy(document_date)
    string_net_amount = net_amount.replace(',','')
    net_amount = Decimal(string_net_amount)
    get_carton_object = ItemUOM.objects.get(itemcode=item_code, uom='CTN')
    carton_rate = get_carton_object.rate
    carton_price = get_carton_object.price
    carton_uom = get_carton_object.uom
    get_unit_object = ItemUOM.objects.get(itemcode=item_code, uom='UNT')
    unit_rate = get_unit_object.rate
    unit_price = get_unit_object.price
    unit_uom = get_unit_object.uom
    description = Item.objects.get(itemcode=item_code).description

    if slash_count == 1: # CTN/UNT
        carton, unit = delivery_qty.split('/')
        carton = int(carton)
        unit = int(unit)
        if not filter_delivery_no:
            with transaction.atomic():
                save_GR = GR(branchautokey=branchautokey,docdate=document_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierdono=delivery_no,description='GOODS RECEIVED NOTE',displayterm=displayterm,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,todoctype='PI',lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount, currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4)
                save_GR.save()
                
                get_gr_guid = GR.objects.filter(supplierdono=delivery_no).first()
                
                if carton > 0:
                    smallest_qty_carton = carton*int(carton_rate)
                    smallest_unit_price_carton = carton_price/carton_rate
                    carton_total_amount = carton * carton_price
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=carton_uom,useruom=carton_uom,qty=carton,rate=carton_rate,smallestqty=smallest_qty_carton,transferedqty=smallest_qty_carton,smallestunitprice=smallest_unit_price_carton,unitprice=carton_price,subtotal=carton_total_amount,localsubtotal=carton_total_amount,subtotalextax=carton_total_amount,deliverydate=document_date,taxableamt=carton_total_amount,localsubtotalextax=carton_total_amount,localtaxableamt=carton_total_amount,taxcurrencytaxableamt=carton_total_amount)
                    save_GR_DTL.save()
                if unit > 0:
                    smallest_qty_unit = unit*int(unit_rate)
                    smallest_unit_price_unit = unit_price/unit_rate
                    unit_total_amount = unit * unit_price
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,transferedqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount)
                    save_GR_DTL.save()
        else:
            get_gr = GR.objects.get(supplierdono=delivery_no)
            get_gr_amount = get_gr.total
            save_gr = False

            if carton > 0:
                filter_grdtl_carton = GRDTL.objects.filter(itemcode=item_code,grautokey=get_gr,uom='CTN')
                smallest_qty_carton = carton*int(carton_rate)
                smallest_unit_price_carton = carton_price/carton_rate
                carton_total_amount = carton * carton_price

                if not filter_grdtl_carton:
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr, itemcode=item_code_instance,location=location_instance,description=description,uom=carton_uom,useruom=carton_uom,qty=carton,rate=carton_rate,smallestqty=smallest_qty_carton,transferedqty=smallest_qty_carton,smallestunitprice=smallest_unit_price_carton,unitprice=carton_price,subtotal=carton_total_amount,localsubtotal=carton_total_amount,subtotalextax=carton_total_amount,deliverydate=document_date,taxableamt=carton_total_amount,localsubtotalextax=carton_total_amount,localtaxableamt=carton_total_amount,taxcurrencytaxableamt=carton_total_amount)
                    save_GR_DTL.save()
                    
                    previous_gr = GR.objects.get(supplierdono=delivery_no)
                    new_value = previous_gr.total + carton_total_amount
                    previous_gr.total = new_value
                    previous_gr.nettotal = new_value
                    previous_gr.localnettotal = new_value
                    previous_gr.analysisnettotal = new_value
                    previous_gr.localanalysisnettotal = new_value
                    previous_gr.totalextax = new_value
                    previous_gr.localtaxableamt = new_value
                    previous_gr.taxcurrencytaxableamt = new_value
                    previous_gr.lastmodified = current_datetime
                    previous_gr.save()
                else:
                    save_gr = True
                    filter_grdtl = GRDTL.objects.get(grautokey=get_gr,itemcode=item_code, uom='CTN')
                    previous_net_amount = filter_grdtl.subtotal
                    get_gr_amount = get_gr_amount - previous_net_amount

                    filter_grdtl.subtotal = carton_total_amount
                    filter_grdtl.localsubtotal = carton_total_amount
                    filter_grdtl.subtotalextax = carton_total_amount
                    filter_grdtl.taxableamt = carton_total_amount
                    filter_grdtl.localsubtotalextax = carton_total_amount
                    filter_grdtl.localtaxableamt = carton_total_amount
                    filter_grdtl.taxcurrencytaxableamt = carton_total_amount
                    filter_grdtl.smallestqty = smallest_qty_carton
                    filter_grdtl.smallestunitprice = smallest_unit_price_carton
                    filter_grdtl.qty = carton
                    filter_grdtl.save()

            if unit>0:
                filter_grdtl_unit = GRDTL.objects.filter(itemcode=item_code,grautokey=get_gr,uom='UNT')
                smallest_qty_unit = unit*int(unit_rate)
                smallest_unit_price_unit = unit_price/unit_rate
                unit_total_amount = unit * unit_price

                if not filter_grdtl_unit:
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,transferedqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount)
                    save_GR_DTL.save()

                    previous_gr = GR.objects.get(supplierdono=delivery_no)
                    new_value = previous_gr.total + unit_total_amount
                    previous_gr.total = new_value
                    previous_gr.nettotal = new_value
                    previous_gr.localnettotal = new_value
                    previous_gr.analysisnettotal = new_value
                    previous_gr.localanalysisnettotal = new_value
                    previous_gr.totalextax = new_value
                    previous_gr.localtaxableamt = new_value
                    previous_gr.taxcurrencytaxableamt = new_value
                    previous_gr.lastmodified = current_datetime
                    previous_gr.save()
                else:
                    save_gr = True
                    filter_grdtl = GRDTL.objects.get(grautokey=get_gr,itemcode=item_code, uom='UNT')
                    get_gr_amount = get_gr_amount - filter_grdtl.subtotal

                    filter_grdtl.subtotal = unit_total_amount
                    filter_grdtl.localsubtotal = unit_total_amount
                    filter_grdtl.subtotalextax = unit_total_amount
                    filter_grdtl.taxableamt = unit_total_amount
                    filter_grdtl.localsubtotalextax = unit_total_amount
                    filter_grdtl.localtaxableamt = unit_total_amount
                    filter_grdtl.taxcurrencytaxableamt = unit_total_amount
                    filter_grdtl.smallestqty = smallest_qty_unit
                    filter_grdtl.smallestunitprice = smallest_unit_price_unit
                    filter_grdtl.qty = unit
                    filter_grdtl.save()

            if save_gr:
                get_gr_amount = get_gr_amount + Decimal(net_amount).quantize(Decimal('0.00'))
                get_gr.total = get_gr_amount
                get_gr.nettotal = get_gr_amount
                get_gr.localnettotal = get_gr_amount
                get_gr.analysisnettotal = get_gr_amount
                get_gr.localanalysisnettotal = get_gr_amount
                get_gr.totalextax = get_gr_amount
                get_gr.localtaxableamt = get_gr_amount
                get_gr.taxcurrencytaxableamt = get_gr_amount
                get_gr.save()

    else: # CTN/BDL/UNT
        get_bundle_object = ItemUOM.objects.get(itemcode=item_code,uom='BDL')
        bundle_rate = get_bundle_object.rate
        bundle_price = get_bundle_object.price
        bundle_uom = get_bundle_object.uom
        carton, bundle, unit = delivery_qty.split('/')
        carton = int(carton)
        bundle = int(bundle)
        unit = int(unit)

        if not filter_delivery_no:
            with transaction.atomic():
                save_GR = GR(branchautokey=branchautokey,docdate=document_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierdono=delivery_no,description='GOODS RECEIVED NOTE',displayterm=displayterm,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,todoctype='PI',lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount, currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4)
                save_GR.save()
                
                get_gr_guid = GR.objects.filter(supplierdono=delivery_no).first()
                
                if carton > 0:
                    smallest_qty_carton = carton*int(carton_rate)
                    smallest_unit_price_carton = carton_price/carton_rate
                    carton_total_amount = carton * carton_price
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=carton_uom,useruom=carton_uom,qty=carton,rate=carton_rate,smallestqty=smallest_qty_carton,transferedqty=smallest_qty_carton,smallestunitprice=smallest_unit_price_carton,unitprice=carton_price,subtotal=carton_total_amount,localsubtotal=carton_total_amount,subtotalextax=carton_total_amount,deliverydate=document_date,taxableamt=carton_total_amount,localsubtotalextax=carton_total_amount,localtaxableamt=carton_total_amount,taxcurrencytaxableamt=carton_total_amount)
                    save_GR_DTL.save()
                if unit > 0:
                    smallest_qty_unit = unit*int(unit_rate)
                    smallest_unit_price_unit = unit_price/unit_rate
                    unit_total_amount = unit * unit_price
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,transferedqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount)
                    save_GR_DTL.save()
                if bundle > 0:
                    smallest_qty_bundle = bundle*int(bundle_rate)
                    smallest_unit_price_bundle = bundle_price/bundle_rate
                    bundle_total_amount = bundle * bundle_price
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=bundle_uom,useruom=bundle_uom,qty=bundle,rate=bundle_rate,smallestqty=smallest_qty_bundle,transferedqty=smallest_qty_bundle,smallestunitprice=smallest_unit_price_bundle,unitprice=bundle_price,subtotal=bundle_total_amount,localsubtotal=bundle_total_amount,subtotalextax=bundle_total_amount,deliverydate=document_date,taxableamt=bundle_total_amount,localsubtotalextax=bundle_total_amount,localtaxableamt=bundle_total_amount,taxcurrencytaxableamt=bundle_total_amount)
                    save_GR_DTL.save()
        else:
            get_gr = GR.objects.get(supplierdono=delivery_no)
            get_gr_amount = get_gr.total
            save_gr = False

            if carton > 0:
                filter_grdtl_carton = GRDTL.objects.filter(itemcode=item_code,grautokey=get_gr,uom='CTN')
                smallest_qty_carton = carton*int(carton_rate)
                smallest_unit_price_carton = carton_price/carton_rate
                carton_total_amount = carton * carton_price

                if not filter_grdtl_carton:
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr, itemcode=item_code_instance,location=location_instance,description=description,uom=carton_uom,useruom=carton_uom,qty=carton,rate=carton_rate,smallestqty=smallest_qty_carton,transferedqty=smallest_qty_carton,smallestunitprice=smallest_unit_price_carton,unitprice=carton_price,subtotal=carton_total_amount,localsubtotal=carton_total_amount,subtotalextax=carton_total_amount,deliverydate=document_date,taxableamt=carton_total_amount,localsubtotalextax=carton_total_amount,localtaxableamt=carton_total_amount,taxcurrencytaxableamt=carton_total_amount)
                    save_GR_DTL.save()
                    
                    previous_gr = GR.objects.get(supplierdono=delivery_no)
                    new_value = previous_gr.total + carton_total_amount
                    previous_gr.total = new_value
                    previous_gr.nettotal = new_value
                    previous_gr.localnettotal = new_value
                    previous_gr.analysisnettotal = new_value
                    previous_gr.localanalysisnettotal = new_value
                    previous_gr.totalextax = new_value
                    previous_gr.localtaxableamt = new_value
                    previous_gr.taxcurrencytaxableamt = new_value
                    previous_gr.lastmodified = current_datetime
                    previous_gr.save()
                else:
                    save_gr = True
                    filter_grdtl = GRDTL.objects.get(grautokey=get_gr,itemcode=item_code, uom='CTN')
                    previous_net_amount = filter_grdtl.subtotal
                    get_gr_amount = get_gr_amount - previous_net_amount

                    filter_grdtl.subtotal = carton_total_amount
                    filter_grdtl.localsubtotal = carton_total_amount
                    filter_grdtl.subtotalextax = carton_total_amount
                    filter_grdtl.taxableamt = carton_total_amount
                    filter_grdtl.localsubtotalextax = carton_total_amount
                    filter_grdtl.localtaxableamt = carton_total_amount
                    filter_grdtl.taxcurrencytaxableamt = carton_total_amount
                    filter_grdtl.smallestqty = smallest_qty_carton
                    filter_grdtl.smallestunitprice = smallest_unit_price_carton
                    filter_grdtl.qty = carton
                    filter_grdtl.save()
            
            if bundle>0:
                filter_grdtl_bundle = GRDTL.objects.filter(itemcode=item_code,grautokey=get_gr, uom='BDL')
                smallest_qty_bundle = bundle*int(bundle_rate)
                smallest_unit_price_bundle = bundle_price/bundle_rate
                bundle_total_amount = bundle * bundle_price

                if not filter_grdtl_bundle:
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr_guid, itemcode=item_code_instance,location=location_instance,description=description,uom=bundle_uom,useruom=bundle_uom,qty=bundle,rate=bundle_rate,smallestqty=smallest_qty_bundle,transferedqty=smallest_qty_bundle,smallestunitprice=smallest_unit_price_bundle,unitprice=bundle_price,subtotal=bundle_total_amount,localsubtotal=bundle_total_amount,subtotalextax=bundle_total_amount,deliverydate=document_date,taxableamt=bundle_total_amount,localsubtotalextax=bundle_total_amount,localtaxableamt=bundle_total_amount,taxcurrencytaxableamt=bundle_total_amount)
                    save_GR_DTL.save()

                    previous_gr = GR.objects.get(supplierdono=delivery_no)
                    new_value = previous_gr.total + bundle_total_amount
                    previous_gr.total = new_value
                    previous_gr.nettotal = new_value
                    previous_gr.localnettotal = new_value
                    previous_gr.analysisnettotal = new_value
                    previous_gr.localanalysisnettotal = new_value
                    previous_gr.totalextax = new_value
                    previous_gr.localtaxableamt = new_value
                    previous_gr.taxcurrencytaxableamt = new_value
                    previous_gr.lastmodified = current_datetime
                    previous_gr.save()
                else:
                    save_gr = True
                    filter_grdtl = GRDTL.objects.get(grautokey=get_gr,itemcode=item_code, uom='BDL')
                    get_gr_amount = get_gr_amount - filter_grdtl.subtotal

                    filter_grdtl.subtotal = bundle_total_amount
                    filter_grdtl.localsubtotal = bundle_total_amount
                    filter_grdtl.subtotalextax = bundle_total_amount
                    filter_grdtl.taxableamt = bundle_total_amount
                    filter_grdtl.localsubtotalextax = bundle_total_amount
                    filter_grdtl.localtaxableamt = bundle_total_amount
                    filter_grdtl.taxcurrencytaxableamt = bundle_total_amount
                    filter_grdtl.smallestqty = smallest_qty_bundle
                    filter_grdtl.smallestunitprice = smallest_unit_price_bundle
                    filter_grdtl.qty = bundle
                    filter_grdtl.save()

            if unit>0:
                filter_grdtl_unit = GRDTL.objects.filter(itemcode=item_code,grautokey=get_gr,uom='UNT')
                smallest_qty_unit = unit*int(unit_rate)
                smallest_unit_price_unit = unit_price/unit_rate
                unit_total_amount = unit * unit_price

                if not filter_grdtl_unit:
                    save_GR_DTL = GRDTL(seq=1,grautokey=get_gr, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,transferedqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount)
                    save_GR_DTL.save()

                    previous_gr = GR.objects.get(supplierdono=delivery_no)
                    new_value = previous_gr.total + unit_total_amount
                    previous_gr.total = new_value
                    previous_gr.nettotal = new_value
                    previous_gr.localnettotal = new_value
                    previous_gr.analysisnettotal = new_value
                    previous_gr.localanalysisnettotal = new_value
                    previous_gr.totalextax = new_value
                    previous_gr.localtaxableamt = new_value
                    previous_gr.taxcurrencytaxableamt = new_value
                    previous_gr.lastmodified = current_datetime
                    previous_gr.save()
                else:
                    save_gr = True
                    filter_grdtl = GRDTL.objects.get(grautokey=get_gr,itemcode=item_code, uom='UNT')
                    get_gr_amount = get_gr_amount - filter_grdtl.subtotal

                    filter_grdtl.subtotal = unit_total_amount
                    filter_grdtl.localsubtotal = unit_total_amount
                    filter_grdtl.subtotalextax = unit_total_amount
                    filter_grdtl.taxableamt = unit_total_amount
                    filter_grdtl.localsubtotalextax = unit_total_amount
                    filter_grdtl.localtaxableamt = unit_total_amount
                    filter_grdtl.taxcurrencytaxableamt = unit_total_amount
                    filter_grdtl.smallestqty = smallest_qty_unit
                    filter_grdtl.smallestunitprice = smallest_unit_price_unit
                    filter_grdtl.qty = unit
                    filter_grdtl.save()
                    

            if save_gr:
                get_gr_amount = get_gr_amount + Decimal(net_amount).quantize(Decimal('0.00'))
                get_gr.total = get_gr_amount
                get_gr.nettotal = get_gr_amount
                get_gr.localnettotal = get_gr_amount
                get_gr.analysisnettotal = get_gr_amount
                get_gr.localanalysisnettotal = get_gr_amount
                get_gr.totalextax = get_gr_amount
                get_gr.localtaxableamt = get_gr_amount
                get_gr.taxcurrencytaxableamt = get_gr_amount
                get_gr.save()
                