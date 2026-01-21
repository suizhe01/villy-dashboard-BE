from debtor.models import Debtor
import datetime
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
from salesagent.models import SalesAgent

def create_mamee_iv_ivdtl(debtor_code,debtor_name,invoice_no,invoice_date,item_code,sales_agent,uom,rate,discount_amount,net_amount,quantity,seq,price, tempcompanyautokey, branchautokey, location, description, temporary_display_term,lorry_driver, udf_book2):
    is_debtor_exist = Debtor.objects.filter(accno=debtor_code).exists()
    is_salesagent_exist = SalesAgent.objects.filter(salesagent=sales_agent).exists()
    # temporary_display_term = Terms.objects.first()
    currency_code = 'MYR'
    allowexceedcreditlimit='T'
    discountpercent = 0
    datetimenow = datetime.datetime.now()
    lastmodifieduserid = 'ADMIN'
    hasbonuspoint='F'
    isgroupcompany = 'F'
    isactive = 'T'
    inclusivetax = 'F'
    filter_invoice_num = IV.objects.filter(docno=invoice_no)
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
    price = Decimal(price).quantize(Decimal('0.00'))
    invoice_date = datetime.datetime.strptime(str(invoice_date), "%Y%m%d")
    # invoice_date = datetime.datetime.strptime(str(invoice_date), "%Y-%m-%dT%H:%M:%S")

    if not is_salesagent_exist:
        new_agent = SalesAgent(salesagent=sales_agent, lastupdate=0,isactive=1)
        new_agent.save()

    if not is_debtor_exist:
        new_debtor = Debtor(accno=debtor_code, companyname=debtor_name, displayterm=temporary_display_term, currencycode=currency_code,allowexceedcreditlimit=allowexceedcreditlimit,discountpercent=discountpercent,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid, hasbonuspoint=hasbonuspoint, isgroupcompany=isgroupcompany,isactive=isactive, lastupdate=0,inclusivetax=inclusivetax,roundingmethod=-1, companyautokey=tempcompanyautokey, selfbilledapprovalno=0)
        new_debtor.save()

    if not filter_invoice_num:
        with transaction.atomic():
            sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            debtor_name_code_instance = Debtor.objects.get(accno=debtor_code)
            new_iv = IV(lorrydriver=lorry_driver,udfbook=udf_book2,displayterm=temporary_display_term,branchautokey=branchautokey,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_name_code_instance,debtorname=debtor_name,description=iv_description,total=net_amount,nettotal=net_amount,localnettotal=net_amount,analysisnettotal=net_amount,finaltotal=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,salesagent=sales_agent,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid,createdtimestamp=datetimenow,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            if discount_amount>0:
                add_to_unit_price = discount_amount/quantity
                unit_price = (net_amount/quantity)+add_to_unit_price
            else:
                unit_price = net_amount/quantity

            smallest_unit_price = Decimal(unit_price).quantize(Decimal('0.00')) /rate
            smallest_qty = Decimal(quantity).quantize(Decimal('0.00'))*rate
            get_iv_object = IV.objects.get(docno=invoice_no) 
            
            new_ivdtl = IVDTL(seq=seq,headerautokey=get_iv_object,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,discount=discount_amount,discountamt=discount_amount,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
            new_ivdtl.save()
    else:
        get_iv_object = IV.objects.get(docno=invoice_no)
        smallest_qty = Decimal(quantity).quantize(Decimal('0.00')) * rate

        if discount_amount>0:
            add_to_unit_price = discount_amount/quantity
            unit_price = (net_amount/quantity)+add_to_unit_price
        else:
            unit_price = net_amount/quantity
        smallest_unit_price = Decimal(unit_price).quantize(Decimal('0.00')) /rate

        new_ivdtl = IVDTL(seq=seq,headerautokey=get_iv_object,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,discount=discount_amount,discountamt=discount_amount,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
        new_ivdtl.save()

        new_value = get_iv_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
        get_iv_object.total = new_value
        get_iv_object.nettotal = new_value
        get_iv_object.localnettotal = new_value
        get_iv_object.analysisnettotal = new_value
        get_iv_object.finaltotal = new_value
        get_iv_object.localtaxableamt = new_value
        get_iv_object.taxcurrencytaxableamt = new_value
        get_iv_object.save()

        