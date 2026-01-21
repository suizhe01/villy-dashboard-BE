from debtor.models import Debtor
from terms.models import Terms
from _lib.panda import current_date_time
from company.models import Company
from cn.models import CN
from django.db import transaction
from branch.models import Branch
from cndtl.models import CNDTL
from location.models import Location
from item.models import Item
from decimal import Decimal
from itemuom.models import ItemUOM
from datetime import datetime
from salesagent.models import SalesAgent

def create_mamee_cn_cndtl(cn_no,cn_date,debtor_code,debtor_name,item_code,uom,quantity,sales_agent,discount_amount,net_amount,seq,temporary_display_term,tempcompanyautokey,branchautokey,location_instance, description):
    is_debtor_exist = Debtor.objects.filter(accno=debtor_code).exists()
    is_salesagent_exist = SalesAgent.objects.filter(salesagent=sales_agent).exists()
    currency_code = 'MYR'
    allowexceedcreditlimit = 'T'
    discountpercent = 0
    datetimenow = current_date_time()
    lastmodifieduserid = 'ADMIN'
    hasbonuspoint='F'
    isgroupcompany = 'F'
    isactive = 'T'
    inclusivetax = 'F'
    filter_cn_number = CN.objects.filter(docno=cn_no)
    iv_description = 'CREDIT NOTE'
    currency_rate = 1
    post_to_stock = 'T'
    post_to_gl = 'T'
    print_out = 0
    cancelled = 'F'
    can_sync = 'F'
    calculate_discount_on_unit_price = 1
    isroundadj = 'F'
    rounding_method = 4
    mainitem = 'T'
    cn_date = datetime.strptime(str(cn_date), "%Y%m%d")
    add_to_subtotal = 'T'
    is_calculate_bonus_point = 'T'
    goods_return = 'T'
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    # print(item_code,uom)
    item_uom_object = ItemUOM.objects.get(itemcode=item_code, uom=uom)
    # price = item_uom_object.price
    rate = item_uom_object.rate

    if not is_salesagent_exist:
        new_agent = SalesAgent(salesagent=sales_agent, lastupdate=0,isactive=1)
        new_agent.save()

    if not is_debtor_exist:
        new_debtor = Debtor(accno=debtor_code, companyname=debtor_name, displayterm=temporary_display_term, currencycode=currency_code,allowexceedcreditlimit=allowexceedcreditlimit,discountpercent=discountpercent,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid, hasbonuspoint=hasbonuspoint, isgroupcompany=isgroupcompany,isactive=isactive, lastupdate=0,inclusivetax=inclusivetax,roundingmethod=-1, companyautokey=tempcompanyautokey, selfbilledapprovalno=0)
        new_debtor.save()

    if not filter_cn_number:
        with transaction.atomic():
            sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            filter_debtor = Debtor.objects.get(accno=debtor_code)
            new_cn = CN(lorrydriver='NA',salesagent=sales_agent,branchautokey=branchautokey,docno=cn_no,docdate=cn_date,debtorcode=filter_debtor,debtorname=debtor_name,description=iv_description,totaxcurrencyrate=1,displayterm=temporary_display_term,total=net_amount,currencycode=currency_code,currencyrate=currency_rate,nettotal=net_amount,localnettotal=net_amount,analysisnettotal=net_amount,localanalysisnettotal=net_amount,posttostock=post_to_stock,posttogl=post_to_gl,printcount=print_out,cancelled=cancelled,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid,createdtimestamp=datetimenow,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=0,calcdiscountonunitprice=calculate_discount_on_unit_price,totalextax=net_amount,inclusivetax=inclusivetax,isroundadj=isroundadj,finaltotal=net_amount,roundingmethod=rounding_method,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
            new_cn.save()

            if discount_amount>0:
                add_to_unit_price = discount_amount/quantity
                unit_price = (net_amount/quantity)+add_to_unit_price
            else:
                unit_price = net_amount/quantity
                
            smallest_unit_price = Decimal(unit_price).quantize(Decimal('0.00'))/rate
            smallestqty = quantity*rate
            get_cn = CN.objects.filter(docno=cn_no).first()

            new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=net_amount,localsubtotal=net_amount,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=net_amount,goodsreturn=goods_return,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,discount=discount_amount,discountamt=discount_amount)
            new_cndtl.save()
    else:
        get_cn_object = CN.objects.get(docno=cn_no)
        smallest_qty = quantity*rate

        if discount_amount>0:
            add_to_unit_price = discount_amount/quantity
            unit_price = (net_amount/quantity)+add_to_unit_price
        else:
            unit_price = net_amount/quantity

        smallest_unit_price = Decimal(unit_price).quantize(Decimal('0.00'))/rate

        new_cndtl = CNDTL(headerautokey=get_cn_object,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=net_amount,localsubtotal=net_amount,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=net_amount,goodsreturn=goods_return,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,discount=discount_amount,discountamt=discount_amount)
        new_cndtl.save()

        new_value = get_cn_object.total + Decimal(net_amount).quantize(Decimal('0.00'))
        get_cn_object.total = new_value
        get_cn_object.nettotal = new_value
        get_cn_object.localnettotal = new_value
        get_cn_object.analysisnettotal = new_value
        get_cn_object.localanalysisnettotal = new_value
        get_cn_object.totalextax = new_value
        get_cn_object.finaltotal = new_value
        get_cn_object.localtaxableamt = new_value
        get_cn_object.taxcurrencytaxableamt = new_value
        get_cn_object.lastmodified = datetimenow
        get_cn_object.save()
