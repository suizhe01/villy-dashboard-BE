from debtor.models import Debtor
from datetime import datetime
from company.models import Company
from iv.models import IV
from branch.models import Branch
from django.db import transaction
from terms.models import Terms
from ivdtl.models import IVDTL
from item.models import Item
from location.models import Location
from decimal import Decimal
from itemuom.models import ItemUOM
from _lib.panda import current_date_time
from salesagent.models import SalesAgent

def create_dob_dksh_iv_ivdtl_invoice(invoice_no,invoice_date,debtor_name,debtor_code,seq,sales_agent,item_code,quantity,uom,discount_amount,net_amount,price,description,temporary_display_term,tempcompanyautokey,branchautokey,location,lorry_driver,udf_book):
    is_debtor_exist = Debtor.objects.filter(accno=debtor_code).exists()
    is_salesagent_exist = SalesAgent.objects.filter(salesagent=sales_agent).exists()
    currency_code = 'MYR'
    allowexceedcreditlimit = 'T'
    discountpercent = 0
    datetimenow = current_date_time()
    lastmodifieduserid = 'ADMIN'
    hasbonuspoint = 'F'
    isgroupcompany = 'F'
    isactive = 'T'
    inclusivetax = 'F'
    filter_invoice_num = IV.objects.filter(docno=invoice_no).exists()
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
    get_uom_object = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
    price = Decimal(price).quantize(Decimal('0.00'))

    # The itemuom row is created by post_dob_dksh_item_itemuom before this runs.
    # Fall back to 1 so a missing row or a rate of 0 cannot divide by zero below.
    rate = get_uom_object.rate if get_uom_object and get_uom_object.rate else 1
    invoice_date = datetime.strptime(str(invoice_date), '%Y-%m-%dT%H:%M:%S')

    if not is_salesagent_exist:
        new_agent = SalesAgent(salesagent=sales_agent, lastupdate=0, isactive=1)
        new_agent.save()

    if not is_debtor_exist:
        new_debtor = Debtor(accno=debtor_code, companyname=debtor_name, displayterm=temporary_display_term, currencycode=currency_code,allowexceedcreditlimit=allowexceedcreditlimit,discountpercent=discountpercent,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid, hasbonuspoint=hasbonuspoint, isgroupcompany=isgroupcompany,isactive=isactive, lastupdate=0,inclusivetax=inclusivetax,roundingmethod=-1, companyautokey=tempcompanyautokey, selfbilledapprovalno=0)
        new_debtor.save()

    if not filter_invoice_num:
        with transaction.atomic():
            sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            debtor_name_code_instance = Debtor.objects.get(accno=debtor_code)
            new_iv = IV(lorrydriver=lorry_driver,udfbook=udf_book,salesagent=sales_agent,displayterm=temporary_display_term,branchautokey=branchautokey,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_name_code_instance,debtorname=debtor_name,description=iv_description,total=net_amount,nettotal=net_amount,localnettotal=net_amount,analysisnettotal=net_amount,finaltotal=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid,createdtimestamp=datetimenow,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            get_iv_guid = IV.objects.get(docno=invoice_no)
            smallest_unit_price = price/rate
            smallest_qty = quantity*rate

            new_ivdtl = IVDTL(seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=price,discount=discount_amount,discountamt=discount_amount,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
            new_ivdtl.save()
    else:
        get_iv_object = IV.objects.get(docno=invoice_no)
        smallest_qty = quantity*rate
        smallest_unit_price = price/rate
        filter_ivdtl = IVDTL.objects.filter(headerautokey=get_iv_object,seq=seq)

        if not filter_ivdtl:
            new_ivdtl = IVDTL(seq=seq,headerautokey=get_iv_object,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=price,discount=discount_amount,discountamt=discount_amount,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
            new_ivdtl.save()

            new_value = get_iv_object.total + Decimal(net_amount).quantize(Decimal('0.0000'))
        else:
            get_ivdtl = IVDTL.objects.get(headerautokey=get_iv_object,seq=seq)
            new_value = get_iv_object.total - get_ivdtl.subtotal + Decimal(net_amount).quantize(Decimal('0.0000'))

            get_ivdtl.itemcode = item_code_instance
            get_ivdtl.description = description
            get_ivdtl.uom = uom
            get_ivdtl.useruom = uom
            get_ivdtl.subtotal = net_amount
            get_ivdtl.localsubtotal = net_amount
            get_ivdtl.subtotalextax = net_amount
            get_ivdtl.taxableamt = net_amount
            get_ivdtl.localsubtotalextax = net_amount
            get_ivdtl.localtaxableamt = net_amount
            get_ivdtl.taxcurrencytaxableamt = net_amount
            get_ivdtl.rate = rate
            get_ivdtl.smallestunitprice = smallest_unit_price
            get_ivdtl.smallestqty = smallest_qty
            get_ivdtl.unitprice = price
            get_ivdtl.discount = discount_amount
            get_ivdtl.discountamt = discount_amount
            get_ivdtl.qty = quantity
            get_ivdtl.save()

        get_iv_object.total = new_value
        get_iv_object.nettotal = new_value
        get_iv_object.localnettotal = new_value
        get_iv_object.analysisnettotal = new_value
        get_iv_object.finaltotal = new_value
        get_iv_object.localtaxableamt = new_value
        get_iv_object.taxcurrencytaxableamt = new_value
        get_iv_object.lastmodified = datetimenow
        get_iv_object.save()
