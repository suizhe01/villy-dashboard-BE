from creditor.models import Creditor
from location.models import Location
from django.db import transaction
from pi.models import PI
from branch.models import Branch
from django.utils import timezone
from pidtl.models import PIDTL
from decimal import Decimal
from gr.models import GR
from item.models import Item
from _lib.panda import convert_date_from_dd_mm_yyyy
from terms.models import Terms
from itemuom.models import ItemUOM

def create_mamee_pi_pidtl(invoice_no, delivery_no,document_date,item_code,delivery_qty,net_amount, slash_count):
    creditor_code_creditor_name = Creditor.objects.filter(companyname='Mamee').first()
    location_instance = Location.objects.filter(location__contains='Mamee').first()
    branchautokey = Branch.objects.filter(address__contains = 'Mamee').first()
    get_gr_docno = GR.objects.filter(supplierdono=delivery_no).first().docno
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    filter_pi = PI.objects.filter(supplierinvoiceno=invoice_no)
    current_datetime = timezone.now()
    document_date = convert_date_from_dd_mm_yyyy(document_date)
    string_net_amount = net_amount.replace(',','')
    net_amount = Decimal(string_net_amount)
    display_term = Terms.objects.first()
    pi_description = 'PURCHASE_INVOICE'
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
        if not filter_pi:
            with transaction.atomic():
                save_PI = PI(branchautokey=branchautokey,docdate=document_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierdono=delivery_no,supplierinvoiceno=invoice_no,description=pi_description,displayterm=display_term,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4, createdtimestamp=current_datetime)
                save_PI.save()

                get_pi_guid = PI.objects.filter(supplierinvoiceno=invoice_no).first()
                
                if carton > 0:
                    smallest_qty_carton = carton*int(carton_rate)
                    smallest_unit_price_carton = carton_price/carton_rate
                    carton_total_amount = carton * carton_price
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=carton_uom,useruom=carton_uom,qty=carton,rate=carton_rate,smallestqty=smallest_qty_carton,smallestunitprice=smallest_unit_price_carton,unitprice=carton_price,subtotal=carton_total_amount,localsubtotal=carton_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=carton_total_amount,deliverydate=document_date,taxableamt=carton_total_amount,localsubtotalextax=carton_total_amount,localtaxableamt=carton_total_amount,taxcurrencytaxableamt=carton_total_amount, transferedqty=0)
                    save_PI_DTL.save()
                if unit > 0:
                    smallest_qty_unit = unit*int(unit_rate)
                    smallest_unit_price_unit = unit_price/unit_rate
                    unit_total_amount = unit * unit_price
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount, transferedqty=0)
                    save_PI_DTL.save()
        else:
            get_pi = PI.objects.get(supplierinvoiceno=invoice_no)
            get_pi_amount = get_pi.total
            save_pi = False

            if carton > 0:
                filter_pidtl_carton = PIDTL.objects.filter(itemcode=item_code,piautokey=get_pi,uom='CTN')
                smallest_qty_carton = carton*int(carton_rate)
                smallest_unit_price_carton = carton_price/carton_rate
                carton_total_amount = carton * carton_price

                if not filter_pidtl_carton:
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount, transferedqty=0)
                    save_PI_DTL.save()

                    previous_pi = PI.objects.get(supplierinvoiceno=invoice_no)
                    new_value = previous_pi.total + carton_total_amount
                    previous_pi.total = new_value
                    previous_pi.nettotal = new_value
                    previous_pi.localnettotal = new_value
                    previous_pi.analysisnettotal = new_value
                    previous_pi.localanalysisnettotal = new_value
                    previous_pi.totalextax = new_value
                    previous_pi.localtaxableamt = new_value
                    previous_pi.taxcurrencytaxableamt = new_value
                    previous_pi.lastmodified = current_datetime
                    previous_pi.save()
                else:
                    save_pi = True
                    filter_pidtl = PIDTL.objects.get(piautokey=get_pi, itemcode=item_code, uom='CTN')
                    previous_net_amount = filter_pidtl.subtotal
                    get_pi_amount = get_pi_amount - previous_net_amount

                    filter_pidtl.subtotal = carton_total_amount
                    filter_pidtl.localsubtotal = carton_total_amount
                    filter_pidtl.subtotalextax = carton_total_amount
                    filter_pidtl.taxableamt = carton_total_amount
                    filter_pidtl.localsubtotalextax = carton_total_amount
                    filter_pidtl.localtaxableamt = carton_total_amount
                    filter_pidtl.taxcurrencytaxableamt = carton_total_amount
                    filter_pidtl.smallestqty = smallest_qty_carton
                    filter_pidtl.smallestunitprice = smallest_unit_price_carton
                    filter_pidtl.qty = carton
                    filter_pidtl.save()

            if unit>0:
                filter_pidtl_unit = PIDTL.objects.filter(itemcode=item_code,piautokey=get_pi,uom='UNT')
                smallest_qty_unit = unit*int(unit_rate)
                smallest_unit_price_unit = unit_price/unit_rate
                unit_total_amount = unit * unit_price

                if not filter_pidtl_unit:
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount, transferedqty=0)
                    save_PI_DTL.save()

                    previous_pi = PI.objects.get(supplierinvoiceno=invoice_no)
                    new_value = previous_pi.total + unit_total_amount
                    previous_pi.total = new_value
                    previous_pi.nettotal = new_value
                    previous_pi.localnettotal = new_value
                    previous_pi.analysisnettotal = new_value
                    previous_pi.localanalysisnettotal = new_value
                    previous_pi.totalextax = new_value
                    previous_pi.localtaxableamt = new_value
                    previous_pi.taxcurrencytaxableamt = new_value
                    previous_pi.lastmodified = current_datetime
                    previous_pi.save()

                else:
                    save_pi = True
                    filter_pidtl = PIDTL.objects.get(piautokey=get_pi,itemcode=item_code,uom='UNT')
                    get_pi_amount = get_pi_amount - filter_pidtl.subtotal
                    filter_pidtl.subtotal = unit_total_amount
                    filter_pidtl.localsubtotal = unit_total_amount
                    filter_pidtl.subtotalextax = unit_total_amount
                    filter_pidtl.taxableamt = unit_total_amount
                    filter_pidtl.localsubtotalextax = unit_total_amount
                    filter_pidtl.localtaxableamt = unit_total_amount
                    filter_pidtl.taxcurrencytaxableamt = unit_total_amount
                    filter_pidtl.smallestqty = smallest_qty_unit
                    filter_pidtl.smallestunitprice = smallest_unit_price_unit
                    filter_pidtl.qty = unit
                    filter_pidtl.save()
                
            if save_pi:
                get_pi_amount = get_pi_amount + Decimal(net_amount).quantize(Decimal('0.00'))
                get_pi.total = get_pi_amount
                get_pi.nettotal = get_pi_amount
                get_pi.localnettotal = get_pi_amount
                get_pi.analysisnettotal = get_pi_amount
                get_pi.localanalysisnettotal = get_pi_amount
                get_pi.totalextax = get_pi_amount
                get_pi.localtaxableamt = get_pi_amount
                get_pi.taxcurrencytaxableamt = get_pi_amount
                get_pi.save()

    else: # CTN/BDL/UNT
        get_bundle_object = ItemUOM.objects.get(itemcode=item_code,uom='BDL')
        bundle_rate = get_bundle_object.rate
        bundle_price = get_bundle_object.price
        bundle_uom = get_bundle_object.uom
        carton, bundle, unit = delivery_qty.split('/')
        carton = int(carton)
        bundle = int(bundle)
        unit = int(unit)
        
        if not filter_pi:
            with transaction.atomic():
                save_PI = PI(branchautokey=branchautokey,docdate=document_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierdono=delivery_no,supplierinvoiceno=invoice_no,description=pi_description,displayterm=display_term,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4, createdtimestamp=current_datetime)
                save_PI.save()

                get_pi_guid = PI.objects.filter(supplierinvoiceno=invoice_no).first()
                
                if carton > 0:
                    smallest_qty_carton = carton*int(carton_rate)
                    smallest_unit_price_carton = carton_price/carton_rate
                    carton_total_amount = carton * carton_price
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=carton_uom,useruom=carton_uom,qty=carton,rate=carton_rate,smallestqty=smallest_qty_carton,smallestunitprice=smallest_unit_price_carton,unitprice=carton_price,subtotal=carton_total_amount,localsubtotal=carton_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=carton_total_amount,deliverydate=document_date,taxableamt=carton_total_amount,localsubtotalextax=carton_total_amount,localtaxableamt=carton_total_amount,taxcurrencytaxableamt=carton_total_amount, transferedqty=0)
                    save_PI_DTL.save()
                if unit > 0:
                    smallest_qty_unit = unit*int(unit_rate)
                    smallest_unit_price_unit = unit_price/unit_rate
                    unit_total_amount = unit * unit_price
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount, transferedqty=0)
                    save_PI_DTL.save()
                if bundle > 0:
                    smallest_qty_bundle = bundle*int(bundle_rate)
                    smallest_unit_price_bundle = bundle_price/bundle_rate
                    bundle_total_amount = bundle * bundle_price
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=bundle_uom,useruom=bundle_uom,qty=bundle,rate=bundle_rate,smallestqty=smallest_qty_bundle,smallestunitprice=smallest_unit_price_bundle,unitprice=bundle_price,subtotal=bundle_total_amount,localsubtotal=bundle_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=bundle_total_amount,deliverydate=document_date,taxableamt=bundle_total_amount,localsubtotalextax=bundle_total_amount,localtaxableamt=bundle_total_amount,taxcurrencytaxableamt=bundle_total_amount, transferedqty=0)
                    save_PI_DTL.save()
        else:
            get_pi = PI.objects.get(supplierinvoice=invoice_no)
            get_pi_amount = get_pi.total
            save_pi = False

            if carton > 0:
                filter_pidtl_carton = PIDTL.objects.filter(itemcode=item_code,piautokey=get_pi,uom='CTN')
                smallest_qty_carton = carton*int(carton_rate)
                smallest_unit_price_carton = carton_price/carton_rate
                carton_total_amount = carton * carton_price

                if not filter_pidtl_carton:
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount, transferedqty=0)
                    save_PI_DTL.save()

                    previous_pi = PI.objects.get(supplierinvoiceno=invoice_no)
                    new_value = previous_pi.total + carton_total_amount
                    previous_pi.total = new_value
                    previous_pi.nettotal = new_value
                    previous_pi.localnettotal = new_value
                    previous_pi.analysisnettotal = new_value
                    previous_pi.localanalysisnettotal = new_value
                    previous_pi.totalextax = new_value
                    previous_pi.localtaxableamt = new_value
                    previous_pi.taxcurrencytaxableamt = new_value
                    previous_pi.lastmodified = current_datetime
                    previous_pi.save()
                else:
                    save_pi = True
                    filter_pidtl = PIDTL.objects.get(piautokey=get_pi, itemcode=item_code, uom='CTN')
                    previous_net_amount = filter_pidtl.subtotal
                    get_pi_amount = get_pi_amount - previous_net_amount

                    filter_pidtl.subtotal = carton_total_amount
                    filter_pidtl.localsubtotal = carton_total_amount
                    filter_pidtl.subtotalextax = carton_total_amount
                    filter_pidtl.taxableamt = carton_total_amount
                    filter_pidtl.localsubtotalextax = carton_total_amount
                    filter_pidtl.localtaxableamt = carton_total_amount
                    filter_pidtl.taxcurrencytaxableamt = carton_total_amount
                    filter_pidtl.smallestqty = smallest_qty_carton
                    filter_pidtl.smallestunitprice = smallest_unit_price_carton
                    filter_pidtl.qty = carton
                    filter_pidtl.save()

            if bundle>0:
                filter_pidtl_bundle = PIDTL.objects.filter(itemcode=item_code, piautokey=get_pi, uom='BDL')
                smallest_qty_bundle = bundle*int(bundle_rate)
                smallest_unit_price_bundle = bundle_price/bundle_rate
                bundle_total_amount = bundle * bundle_price

                if not filter_pidtl_bundle:
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=bundle_uom,useruom=bundle_uom,qty=bundle,rate=bundle_rate,smallestqty=smallest_qty_bundle,smallestunitprice=smallest_unit_price_bundle,unitprice=bundle_price,subtotal=bundle_total_amount,localsubtotal=bundle_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=bundle_total_amount,deliverydate=document_date,taxableamt=bundle_total_amount,localsubtotalextax=bundle_total_amount,localtaxableamt=bundle_total_amount,taxcurrencytaxableamt=bundle_total_amount, transferedqty=0)
                    save_PI_DTL.save()

                    previous_pi = PI.objects.get(supplierinvoice=invoice_no)
                    new_value = previous_pi.total + bundle_total_amount
                    previous_pi.total = new_value
                    previous_pi.nettotal = new_value
                    previous_pi.localnettotal = new_value
                    previous_pi.analysisnettotal = new_value
                    previous_pi.localanalysisnettotal = new_value
                    previous_pi.totalextax = new_value
                    previous_pi.localtaxableamt = new_value
                    previous_pi.taxcurrencytaxableamt = new_value
                    previous_pi.lastmodified = current_datetime
                    previous_pi.save()
            else:
                save_pi = True
                filter_pidtl = PIDTL.objects.get(piautokey=get_pi,itemcode=item_code, uom='BDL')
                get_pi_amount = get_pi_amount - filter_pidtl.subtotal

                filter_pidtl.subtotal = bundle_total_amount
                filter_pidtl.localsubtotal = bundle_total_amount
                filter_pidtl.subtotalextax = bundle_total_amount
                filter_pidtl.taxableamt = bundle_total_amount
                filter_pidtl.localsubtotalextax = bundle_total_amount
                filter_pidtl.localtaxableamt = bundle_total_amount
                filter_pidtl.taxcurrencytaxableamt = bundle_total_amount
                filter_pidtl.smallestqty = smallest_qty_bundle
                filter_pidtl.smallestunitprice = smallest_unit_price_bundle
                filter_pidtl.qty = bundle
                filter_pidtl.save()

            if unit>0:
                filter_pidtl_unit = PIDTL.objects.filter(itemcode=item_code,piautokey=get_pi,uom='UNT')
                smallest_qty_unit = unit*int(unit_rate)
                smallest_unit_price_unit = unit_price/unit_rate
                unit_total_amount = unit * unit_price

                if not filter_pidtl_unit:
                    save_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit,rate=unit_rate,smallestqty=smallest_qty_unit,smallestunitprice=smallest_unit_price_unit,unitprice=unit_price,subtotal=unit_total_amount,localsubtotal=unit_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=unit_total_amount,deliverydate=document_date,taxableamt=unit_total_amount,localsubtotalextax=unit_total_amount,localtaxableamt=unit_total_amount,taxcurrencytaxableamt=unit_total_amount, transferedqty=0)
                    save_PI_DTL.save()

                    previous_pi = PI.objects.get(supplierinvoiceno=invoice_no)
                    new_value = previous_pi.total + unit_total_amount
                    previous_pi.total = new_value
                    previous_pi.nettotal = new_value
                    previous_pi.localnettotal = new_value
                    previous_pi.analysisnettotal = new_value
                    previous_pi.localanalysisnettotal = new_value
                    previous_pi.totalextax = new_value
                    previous_pi.localtaxableamt = new_value
                    previous_pi.taxcurrencytaxableamt = new_value
                    previous_pi.lastmodified = current_datetime
                    previous_pi.save()

                else:
                    save_pi = True
                    filter_pidtl = PIDTL.objects.get(piautokey=get_pi,itemcode=item_code,uom='UNT')
                    get_pi_amount = get_pi_amount - filter_pidtl.subtotal
                    filter_pidtl.subtotal = unit_total_amount
                    filter_pidtl.localsubtotal = unit_total_amount
                    filter_pidtl.subtotalextax = unit_total_amount
                    filter_pidtl.taxableamt = unit_total_amount
                    filter_pidtl.localsubtotalextax = unit_total_amount
                    filter_pidtl.localtaxableamt = unit_total_amount
                    filter_pidtl.taxcurrencytaxableamt = unit_total_amount
                    filter_pidtl.smallestqty = smallest_qty_unit
                    filter_pidtl.smallestunitprice = smallest_unit_price_unit
                    filter_pidtl.qty = unit
                    filter_pidtl.save()
                
            if save_pi:
                get_pi_amount = get_pi_amount + Decimal(net_amount).quantize(Decimal('0.00'))
                get_pi.total = get_pi_amount
                get_pi.nettotal = get_pi_amount
                get_pi.localnettotal = get_pi_amount
                get_pi.analysisnettotal = get_pi_amount
                get_pi.localanalysisnettotal = get_pi_amount
                get_pi.totalextax = get_pi_amount
                get_pi.localtaxableamt = get_pi_amount
                get_pi.taxcurrencytaxableamt = get_pi_amount
                get_pi.save()
