from _lib.panda import current_date_time
from debtor.models import Debtor
from company.models import Company
from iv.models import IV
from branch.models import Branch
from django.db import transaction
from terms.models import Terms
from ivdtl.models import IVDTL
from item.models import Item
import datetime
from decimal import Decimal
from itemuom.models import ItemUOM
from location.models import Location
from salesagent.models import SalesAgent

def create_dob_yltc_iv_ivdtl_invoice(debtor_code, debtor_name,invoice_no,item_code,invoice_date,delivery_date,quantity,total_price,discount_amt,net_amount, uom,seq,price, sales_agent, description, rate, tempcompanyautokey, branchautokey, location, temporary_display_term,lorry_driver,udf_book):
    is_debtor_exist = Debtor.objects.filter(accno=debtor_code).exists()
    is_salesagent_exist = SalesAgent.objects.filter(salesagent=sales_agent).exists()
    currency_code = 'MYR'
    # temporary_display_term = Terms.objects.first()
    currency_code = 'MYR'
    allowexceedcreditlimit='T'
    datetimenow = current_date_time()
    lastmodifieduserid = 'ADMIN'
    hasbonuspoint='F'
    isgroupcompany = 'F'
    isactive = 'T'
    inclusivetax = 'F'
    delivery_date = datetime.datetime.strptime(str(delivery_date), '%Y%m%d').date()
    filter_invoice_num = IV.objects.filter(docno=invoice_no)
    # branchautokey = Branch.objects.filter(address__contains = 'Redbull').first()
    rounding_method = 4
    to_tax_currency_rate = 1
    currency_rate = 1
    post_to_stock = 'T'
    post_to_gl = 'T'
    transferable = 'T'
    print_count = 0
    cancelled = 'F'
    can_sync = 'F'
    last_update = 0
    reallocate_purchase_by_project = 'F'
    iv_description = 'INVOICE'
    main_item = 'T'
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    # location = Location.objects.filter(location='Redbull').first()
    selfbilledapprovalno = 0
    rounding_method = -1
    price = Decimal(price).quantize(Decimal('0.00'))
    invoice_date = datetime.datetime.strptime(str(invoice_date), '%Y%m%d')

    if not is_salesagent_exist:
        new_agent = SalesAgent(salesagent=sales_agent, lastupdate=0,isactive=1)
        new_agent.save()

    if not is_debtor_exist:
        new_debtor = Debtor(accno=debtor_code, companyname=debtor_name, displayterm=temporary_display_term, currencycode=currency_code,allowexceedcreditlimit=allowexceedcreditlimit,discountpercent=0,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid, hasbonuspoint=hasbonuspoint, isgroupcompany=isgroupcompany,isactive=isactive, lastupdate=0,inclusivetax=inclusivetax,roundingmethod=rounding_method, companyautokey=tempcompanyautokey, selfbilledapprovalno=selfbilledapprovalno)
        new_debtor.save()

    if not filter_invoice_num:
        with transaction.atomic():
            sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            debtor_name_code_instance = Debtor.objects.get(accno=debtor_code)
            new_iv = IV(lorrydriver=lorry_driver,udfbook=udf_book,salesagent=sales_agent,displayterm=temporary_display_term,branchautokey=branchautokey,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_name_code_instance,debtorname=debtor_name,description=iv_description,total=net_amount,nettotal=net_amount,localnettotal=net_amount,analysisnettotal=net_amount,finaltotal=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid,createdtimestamp=datetimenow,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            if discount_amt>0:
                add_to_unit_price = discount_amt/quantity
                unit_price = (net_amount/quantity)+add_to_unit_price
            else:
                unit_price = net_amount/quantity

            smallest_unit_price =  Decimal(unit_price).quantize(Decimal('0.00'))/rate
            get_iv_guid = IV.objects.get(docno=invoice_no)
            smallest_qty = quantity*rate

            new_ivdtl = IVDTL(seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=price,discount=discount_amt,discountamt=discount_amt,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,deliverydate=delivery_date,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
            new_ivdtl.save()
    else:
        get_iv_object = IV.objects.get(docno=invoice_no)
        smallest_qty = quantity*rate

        if discount_amt>0:
            add_to_unit_price = discount_amt/quantity
            unit_price = (net_amount/quantity)+add_to_unit_price
        else:
            unit_price = net_amount/quantity

        smallest_unit_price = Decimal(unit_price).quantize(Decimal('0.00'))/rate

        # if float(net_amount)>0:
        # filter_ivdtl = IVDTL.objects.filter(itemcode=item_code_instance,headerautokey=get_iv_object,subtotal__gt=0)
        # if not filter_ivdtl:
        new_ivdtl = IVDTL(seq=seq,headerautokey=get_iv_object,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=price,discount=discount_amt,discountamt=discount_amt,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,deliverydate=delivery_date,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
        new_ivdtl.save()

        new_value = get_iv_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
        get_iv_object.total = new_value
        get_iv_object.nettotal = new_value
        get_iv_object.localnettotal = new_value
        get_iv_object.analysisnettotal = new_value
        get_iv_object.localanalysisnettotal = new_value
        get_iv_object.totalextax = new_value
        get_iv_object.finaltotal = new_value
        get_iv_object.localtaxableamt = new_value
        get_iv_object.taxcurrencytaxableamt = new_value
        get_iv_object.lastmodified = datetimenow
        get_iv_object.save()