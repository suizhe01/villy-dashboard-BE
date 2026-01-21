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

def create_cola_iv_ivdtl(debtor_code,debtor_name,invoice_no,invoice_date,seq, item_code,quantity,uom, rate,discount_amount,net_amount,total_invoice_amount,price, sales_agent,tempcompanyautokey, branchautokey, location, description, temporary_display_term,lorry_driver, udf_book2):
    is_debtor_exist = Debtor.objects.filter(accno=debtor_code).exists()
    is_salesagent_exist = SalesAgent.objects.filter(salesagent=sales_agent).exists()
    currency_code = 'MYR'
    allowexceedcreditlimit='T'
    discountpercent = 0
    datetimenow = current_date_time()
    lastmodifieduserid = 'ADMIN'
    hasbonuspoint='F'
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

    if 'T' in invoice_date:
        invoice_date = invoice_date.split('T')[0]
    
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
            new_iv = IV(lorrydriver=lorry_driver,udfbook=udf_book2,salesagent=sales_agent,displayterm=temporary_display_term,branchautokey=branchautokey,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_name_code_instance,debtorname=debtor_name,description=iv_description,total=total_invoice_amount,nettotal=total_invoice_amount,localnettotal=total_invoice_amount,analysisnettotal=total_invoice_amount,finaltotal=total_invoice_amount,localtaxableamt=total_invoice_amount,taxcurrencytaxableamt=total_invoice_amount,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid,createdtimestamp=datetimenow,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            if discount_amount>0:
                add_to_unit_price = discount_amount/quantity
                unit_price = (net_amount/quantity)+add_to_unit_price
            else: 
                unit_price = net_amount/quantity
            
            smallest_unit_price = Decimal(unit_price).quantize(Decimal('0.00'))/rate

            get_iv_guid = IV.objects.get(docno=invoice_no)
            smallest_qty = quantity*rate

            new_ivdtl = IVDTL(seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,discount=discount_amount,discountamt=discount_amount,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
            new_ivdtl.save()
    else:
        get_iv_object = IV.objects.get(docno=invoice_no)
        # get_iv_object.docdate = invoice_date
        # get_iv_object.save()
        smallest_qty = quantity*rate

        if discount_amount>0:
            add_to_unit_price = discount_amount/quantity
            unit_price = (net_amount/quantity)+add_to_unit_price
        else:
            unit_price = net_amount/quantity

        smallest_unit_price = Decimal(unit_price).quantize(Decimal('0.00'))/rate

        filter_ivdtl = IVDTL.objects.filter(headerautokey=get_iv_object,seq=seq)
        
        if not filter_ivdtl:
            new_ivdtl = IVDTL(seq=seq,headerautokey=get_iv_object,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,discount=discount_amount,discountamt=discount_amount,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
            new_ivdtl.save()
        else:
            get_ivdtl = IVDTL.objects.get(headerautokey=get_iv_object,seq=seq)
            get_ivdtl.subtotal = net_amount
            get_ivdtl.localsubtotal = net_amount
            get_ivdtl.subtotalextax = net_amount
            get_ivdtl.taxableamt = net_amount
            get_ivdtl.localsubtotalextax = net_amount
            get_ivdtl.localtaxableamt = net_amount
            get_ivdtl.taxcurrencytaxableamt = net_amount
            get_ivdtl.smallestunitprice = smallest_unit_price
            get_ivdtl.smallestqty = smallest_qty
            get_ivdtl.unitprice = unit_price
            get_ivdtl.discount = discount_amount
            get_ivdtl.discountamt = discount_amount
            get_ivdtl.qty = quantity
            get_ivdtl.save()

