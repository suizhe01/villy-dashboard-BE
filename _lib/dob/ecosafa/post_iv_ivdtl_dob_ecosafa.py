from _lib.panda import current_date_time
from debtor.models import Debtor
from company.models import Company
from iv.models import IV
from terms.models import Terms
from ivdtl.models import IVDTL
from item.models import Item
from itemuom.models import ItemUOM
from location.models import Location
from salesagent.models import SalesAgent
from django.db import transaction
from decimal import Decimal
import datetime

def create_dob_ecosafa_iv_ivdtl_invoice(debtor_code, debtor_name, invoice_no, item_code, invoice_date, quantity, rate, uom, seq, tempcompanyautokey, branchautokey, location, temporary_display_term, lorry_driver, udf_book, description):
    net_amount = 0
    price = 0
    sales_agent = 'NA'

    is_debtor_exist = Debtor.objects.filter(accno=debtor_code).exists()
    is_salesagent_exist = SalesAgent.objects.filter(salesagent=sales_agent).exists()

    currency_code = 'MYR'
    currency_rate = 1
    allowexceedcreditlimit = 'T'
    datetimenow = current_date_time()
    lastmodifieduserid = 'ADMIN'
    hasbonuspoint = 'F'
    isgroupcompany = 'F'
    isactive = 'T'
    inclusivetax = 'F'
    post_to_stock = 'T'
    post_to_gl = 'T'
    transferable = 'T'
    print_count = 0
    cancelled = 'F'
    can_sync = 'F'
    last_update = 0
    reallocate_purchase_by_project = 'F'
    to_tax_currency_rate = 1
    rounding_method = -1
    iv_description = 'INVOICE'
    main_item = 'T'
    selfbilledapprovalno = 0

    invoice_date = datetime.datetime.strptime(str(invoice_date), '%Y-%m-%dT%H:%M:%S')
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    filter_invoice_num = IV.objects.filter(docno=invoice_no)

    if not is_salesagent_exist:
        new_agent = SalesAgent(salesagent=sales_agent, lastupdate=0, isactive=1)
        new_agent.save()

    if not is_debtor_exist:
        new_debtor = Debtor(accno=debtor_code, companyname=debtor_name, displayterm=temporary_display_term, currencycode=currency_code, allowexceedcreditlimit=allowexceedcreditlimit, discountpercent=0, lastmodified=datetimenow, lastmodifieduserid=lastmodifieduserid, hasbonuspoint=hasbonuspoint, isgroupcompany=isgroupcompany, isactive=isactive, lastupdate=0, inclusivetax=inclusivetax, roundingmethod=rounding_method, companyautokey=tempcompanyautokey, selfbilledapprovalno=selfbilledapprovalno)
        new_debtor.save()

    sales_agent_instance = SalesAgent.objects.get(salesagent=sales_agent)
    debtor_instance = Debtor.objects.get(accno=debtor_code)

    if not filter_invoice_num:
        with transaction.atomic():
            new_iv = IV(lorrydriver=lorry_driver, udfbook=udf_book, salesagent=sales_agent_instance, displayterm=temporary_display_term, branchautokey=branchautokey, docno=invoice_no, docdate=invoice_date, debtorcode=debtor_instance, debtorname=debtor_name, description=iv_description, total=net_amount, nettotal=net_amount, localnettotal=net_amount, analysisnettotal=net_amount, finaltotal=net_amount, localtaxableamt=net_amount, taxcurrencytaxableamt=net_amount, currencycode=currency_code, currencyrate=currency_rate, posttostock=post_to_stock, posttogl=post_to_gl, transferable=transferable, printcount=print_count, cancelled=cancelled, lastmodified=datetimenow, lastmodifieduserid=lastmodifieduserid, createdtimestamp=datetimenow, createduserid=lastmodifieduserid, cansync=can_sync, lastupdate=last_update, reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate, roundingmethod=rounding_method)
            new_iv.save()

            get_iv_guid = IV.objects.get(docno=invoice_no)
            smallest_qty = quantity * rate
            smallest_unit_price = 0

            new_ivdtl = IVDTL(seq=seq, headerautokey=get_iv_guid, mainitem=main_item, itemcode=item_code_instance, description=description, uom=uom, useruom=uom, qty=quantity, rate=rate, smallestqty=smallest_qty, transferedqty=rate, smallestunitprice=smallest_unit_price, unitprice=price, subtotal=net_amount, localsubtotal=net_amount, subtotalextax=net_amount, location=location, taxableamt=net_amount, localsubtotalextax=net_amount, localtaxableamt=net_amount, taxcurrencytaxableamt=net_amount)
            new_ivdtl.save()
    else:
        get_iv_object = IV.objects.get(docno=invoice_no)
        smallest_qty = quantity * rate
        smallest_unit_price = 0

        new_ivdtl = IVDTL(seq=seq, headerautokey=get_iv_object, mainitem=main_item, itemcode=item_code_instance, description=description, uom=uom, useruom=uom, qty=quantity, rate=rate, smallestqty=smallest_qty, transferedqty=rate, smallestunitprice=smallest_unit_price, unitprice=price, subtotal=net_amount, localsubtotal=net_amount, subtotalextax=net_amount, location=location, taxableamt=net_amount, localsubtotalextax=net_amount, localtaxableamt=net_amount, taxcurrencytaxableamt=net_amount)
        new_ivdtl.save()

        get_iv_object.lastmodified = datetimenow
        get_iv_object.save()
