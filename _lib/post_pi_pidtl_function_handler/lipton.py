from gr.models import GR
from pi.models import PI
from pidtl.models import PIDTL
from item.models import Item
from branch.models import Branch
from creditor.models import Creditor
from location.models import Location
from django.db import transaction
from decimal import Decimal
from terms.models import Terms
from _lib.panda import current_date_time
from itemuom.models import ItemUOM
from datetime import datetime

def create_lipton_pi_pidtl(purchase_invoice_date,product_expiry_date,item_code,purchase_invoice_no,net_amount,quantity,description,uom):
    displayterm = Terms.objects.first()
    creditor_code_creditor_name = Creditor.objects.filter(companyname='Lipton').first()
    location_instance = Location.objects.filter(location__contains='Lipton').first()
    branchautokey = Branch.objects.filter(address__contains = 'Lipton').first()
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    filter_pi = PI.objects.filter(supplierinvoiceno=purchase_invoice_no)
    purchase_invoice_date = datetime.strptime(purchase_invoice_date, "%d-%m-%y")
    product_expiry_date = datetime.strptime(product_expiry_date, "%d-%m-%y")
    current_datetime = current_date_time()
    item_object = ItemUOM.objects.get(itemcode=item_code,uom=uom)
    rate = item_object.rate
    price = item_object.price

    if not filter_pi:
        with transaction.atomic():
            SAVE_PI = PI(branchautokey=branchautokey,docdate=purchase_invoice_date,creditorcode=creditor_code_creditor_name,creditorname=creditor_code_creditor_name,supplierinvoiceno=purchase_invoice_no,description='PURCHASE_INVOICE',displayterm=displayterm,total=net_amount,currencycode='MYR',nettotal=net_amount,localnettotal=net_amount,lastmodified=current_datetime,analysisnettotal=net_amount,localanalysisnettotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,currencyrate=1,printcount=0,lastupdate=0, totaxcurrencyrate=1,roundingmethod=4, createdtimestamp=current_datetime)
            SAVE_PI.save()

            get_pi_guid = PI.objects.filter(supplierinvoiceno=purchase_invoice_no).first()
            smallest_qty = int(quantity)*int(rate)
            smallest_unit_price = price/rate

            SAVE_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,desc2=product_expiry_date,transferedqty=0)
            SAVE_PI_DTL.save()
    else:
        previous_pi_object = PI.objects.get(supplierinvoiceno = purchase_invoice_no)
        new_value = previous_pi_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
        previous_pi_object.total = new_value
        previous_pi_object.nettotal = new_value
        previous_pi_object.localnettotal = new_value
        previous_pi_object.analysisnettotal = new_value
        previous_pi_object.localanalysisnettotal = new_value
        previous_pi_object.totalextax = new_value
        previous_pi_object.finaltotal = new_value
        previous_pi_object.localtaxableamt = new_value
        previous_pi_object.taxcurrencytaxableamt = new_value
        previous_pi_object.lastmodified = current_datetime
        previous_pi_object.save()

        get_pi_guid = PI.objects.filter(supplierinvoiceno=purchase_invoice_no).first()
        smallest_qty = int(quantity)*int(rate)
        smallest_unit_price = price/rate

        # what is seq use for?
        SAVE_PI_DTL = PIDTL(piautokey=get_pi_guid,seq=1, itemcode=item_code_instance,location=location_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,desc2=product_expiry_date,transferedqty=0)
        SAVE_PI_DTL.save()