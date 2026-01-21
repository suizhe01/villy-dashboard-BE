from django.db import transaction
from pi.models import PI
from branch.models import Branch
from pidtl.models import PIDTL
from decimal import Decimal
from gr.models import GR
from item.models import Item
from _lib.panda import current_date_time
from creditor.models import Creditor
from location.models import Location
from terms.models import Terms
from itemuom.models import ItemUOM
from django.core.exceptions import ObjectDoesNotExist

def create_dutchlady_pi_pidtl_purchase(invoice_date,delivery_no,delivery_date,invoice_no,net_amount,received_qty,item_code,batch_no,uom,expiry_date):
    displayterm = Terms.objects.first()
    get_gr_docno = GR.objects.filter(supplierdono=delivery_no).first().docno
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    filter_pi = PI.objects.filter(supplierinvoiceno=invoice_no)
    current_datetime = current_date_time()
    branchautokey = Branch.objects.filter(address__contains = 'Dutch Lady').first()
    creditor_code_creditor_name = Creditor.objects.filter(companyname='Dutch Lady').first()
    location_instance = Location.objects.filter(location__contains='Dutch Lady').first()
    try:
        get_uom_object = ItemUOM.objects.get(itemcode=item_code, uom=uom)
    except ObjectDoesNotExist:
        return f"UOM or item code does not exist."
    rate = get_uom_object.rate
    price = get_uom_object.price
    get_item = Item.objects.get(itemcode=item_code)
    description = get_item.description

    if not filter_pi:
        with transaction.atomic():
            save_PI_DTL = PI(branchautokey=branchautokey,docdate=invoice_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierdono=delivery_no,supplierinvoiceno=invoice_no,description='PURCHASE_INVOICE',displayterm=displayterm,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4, createdtimestamp=current_datetime)
            save_PI_DTL.save()

            get_pi_guid = PI.objects.get(supplierinvoiceno=invoice_no)
            smallest_qty_box = received_qty*int(rate)
            smallest_unit_price_box = price/rate
            # box_total_amount = received_qty * price
            save_PI_DTL_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,batchno=batch_no,description=description,uom=uom,useruom=uom,qty=received_qty,rate=rate,smallestqty=smallest_qty_box,smallestunitprice=smallest_unit_price_box,unitprice=price,subtotal=net_amount,localsubtotal=net_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=net_amount,deliverydate=delivery_date,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,desc2=expiry_date,transferedqty=0)
            save_PI_DTL_DTL.save()
    else:
        get_pi_object = PI.objects.get(supplierinvoiceno=invoice_no)
        filter_pi_pidtl = PIDTL.objects.filter(itemcode=item_code,piautokey=get_pi_object,batchno=batch_no)
        smallest_qty_box = received_qty*int(rate)
        smallest_unit_price_box = price/rate
        get_pi_guid = PI.objects.get(supplierinvoiceno=invoice_no)

        if not filter_pi_pidtl:
            new_pi_pidtl = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,batchno=batch_no,description=description,uom=uom,useruom=uom,qty=received_qty,rate=rate,smallestqty=smallest_qty_box,smallestunitprice=smallest_unit_price_box,unitprice=price,subtotal=net_amount,localsubtotal=net_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=net_amount,deliverydate=delivery_date,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,desc2=expiry_date,transferedqty=0)
            new_pi_pidtl.save()

            new_value = get_pi_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
            get_pi_object.total = new_value
            get_pi_object.nettotal = new_value
            get_pi_object.localnettotal = new_value
            get_pi_object.analysisnettotal = new_value
            get_pi_object.localanalysisnettotal = new_value
            get_pi_object.totalextax = new_value
            get_pi_object.finaltotal = new_value
            get_pi_object.localtaxableamt = new_value
            get_pi_object.taxcurrencytaxableamt = new_value
            get_pi_object.lastmodified = current_datetime
            get_pi_object.save()
        else:
            get_pi_amount = get_pi_object.total
            filter_pi_pidtl_object = PIDTL.objects.get(itemcode=item_code,piautokey=get_pi_object,batchno=batch_no)
            previous_pidtl_net_amount = filter_pi_pidtl_object.subtotal
            get_new_pi_amount = get_pi_amount - previous_pidtl_net_amount + Decimal(net_amount).quantize(Decimal('0.00'))

            filter_pi_pidtl_object.qty = net_amount
            filter_pi_pidtl_object.subtotal = net_amount
            filter_pi_pidtl_object.localsubtotal = net_amount
            filter_pi_pidtl_object.subtotalextax = net_amount
            filter_pi_pidtl_object.taxableamt = net_amount
            filter_pi_pidtl_object.localsubtotalextax = net_amount
            filter_pi_pidtl_object.localtaxableamt = net_amount
            filter_pi_pidtl_object.taxcurrencytaxableamt = net_amount
            filter_pi_pidtl_object.save()

            get_pi_object.total = get_new_pi_amount
            get_pi_object.nettotal = get_new_pi_amount
            get_pi_object.localnettotal = get_new_pi_amount
            get_pi_object.analysisnettotal = get_new_pi_amount
            get_pi_object.localanalysisnettotal = get_new_pi_amount
            get_pi_object.totalextax = get_new_pi_amount
            get_pi_object.finaltotal = get_new_pi_amount
            get_pi_object.localtaxableamt = get_new_pi_amount
            get_pi_object.taxcurrencytaxableamt = get_new_pi_amount
            get_pi_object.lastmodified = current_datetime
            get_pi_object.save()

        # get_pi_guid = PI.objects.filter(supplierinvoiceno=invoice_no).first()
        # smallest_qty_box = received_qty*int(rate)
        # smallest_unit_price_box = price/rate
        # box_total_amount = received_qty * price
        # save_PI_DTL_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,batchno=batch_no,description=description,uom=uom,useruom=uom,qty=received_qty,rate=rate,smallestqty=smallest_qty_box,smallestunitprice=smallest_unit_price_box,unitprice=price,subtotal=box_total_amount,localsubtotal=box_total_amount,fromdoctype='GR',fromdocno=get_gr_docno,subtotalextax=box_total_amount,deliverydate=delivery_date,taxableamt=box_total_amount,localsubtotalextax=box_total_amount,localtaxableamt=box_total_amount,taxcurrencytaxableamt=box_total_amount,desc2=expiry_date,transferedqty=0)
        # save_PI_DTL_DTL.save()

    return 'success'