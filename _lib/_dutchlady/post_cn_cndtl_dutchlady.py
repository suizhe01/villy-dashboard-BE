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
from salesagent.models import SalesAgent

def create_dutchlady_cn_cndtl(sales_agent,cn_no,  cn_date, debtor_code, debtor_name, item_code, box_qty, unit_qty, total_amount, discount_amount ,net_amount, seq, box_price, unit_price,temporary_display_term,tempcompanyautokey,branchautokey,location_instance,box_rate,box_uom,unit_rate,unit_uom,description,our_invoice_no):
    is_debtor_exist = Debtor.objects.filter(accno=debtor_code).exists()
    is_salesagent_exist = SalesAgent.objects.filter(salesagent=sales_agent).exists()
    currency_code = 'MYR'
    currency_code = 'MYR'
    allowexceedcreditlimit = 'T'
    discountpercent = 0
    datetimenow = current_date_time()
    lastmodifieduserid = 'ADMIN'
    hasbonuspoint='F'
    isgroupcompany = 'F'
    isactive = 'T'
    inclusivetax = 'F'
    filter_cn_number = CN.objects.filter(docno=cn_no).exists()
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
    add_to_subtotal = 'T'
    is_calculate_bonus_point = 'T'
    goods_return = 'T'
    item_code_instance = Item.objects.filter(itemcode=item_code).first()
    item_code_object = Item.objects.get(itemcode=item_code)
    box_price = Decimal(box_price).quantize(Decimal('0.0000'))
    unit_price = Decimal(unit_price).quantize(Decimal('0.0000'))

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
            debtor_name = filter_debtor.companyname
            new_cn = CN(lorrydriver='NA',salesagent=sales_agent,branchautokey=branchautokey,docno=cn_no,docdate=cn_date,debtorcode=filter_debtor,debtorname=debtor_name,description=iv_description,totaxcurrencyrate=1,displayterm=temporary_display_term,total=net_amount,currencycode=currency_code,currencyrate=currency_rate,nettotal=net_amount,localnettotal=net_amount,analysisnettotal=net_amount,localanalysisnettotal=net_amount,posttostock=post_to_stock,posttogl=post_to_gl,printcount=print_out,cancelled=cancelled,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid,createdtimestamp=datetimenow,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=0,calcdiscountonunitprice=calculate_discount_on_unit_price,totalextax=net_amount,inclusivetax=inclusivetax,isroundadj=isroundadj,finaltotal=net_amount,roundingmethod=rounding_method,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,ourinvoiceno=our_invoice_no)
            new_cn.save()

            get_cn = CN.objects.filter(docno=cn_no).first()

            enter_unit_discount = True

            if box_qty >0:
                smallest_qty = box_qty*box_rate
                smallest_unit_price = box_price/box_rate
                total_box_price = box_price * box_qty
                if discount_amount>0.0:
                    enter_unit_discount = False
                    total_box_price = total_box_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=box_uom,useruom=box_uom,qty=box_qty,rate=box_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=box_price,subtotal=total_box_price,localsubtotal=total_box_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_box_price,goodsreturn=goods_return,taxableamt=total_box_price,localsubtotalextax=total_box_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_box_price,taxcurrencytaxableamt=total_box_price)
                    new_cndtl.save()
                else:
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=box_uom,useruom=box_uom,qty=box_qty,rate=box_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=box_price,subtotal=total_box_price,localsubtotal=total_box_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_box_price,goodsreturn=goods_return,taxableamt=total_box_price,localsubtotalextax=total_box_price,discount=0,discountamt=0,localtaxableamt=total_box_price,taxcurrencytaxableamt=total_box_price)
                    new_cndtl.save()

            if unit_qty >0:
                smallest_qty = unit_qty*unit_rate
                smallest_unit_price = unit_price/unit_rate
                total_unit_price = unit_price * unit_qty
                
                if discount_amount>0.0:
                    if not enter_unit_discount:
                        discount_amount = 0
                    total_unit_price = total_unit_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit_qty,rate=unit_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_unit_price,goodsreturn=goods_return,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price)
                    new_cndtl.save()
                else:
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit_qty,rate=unit_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_unit_price,goodsreturn=goods_return,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discount=0,discountamt=0,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price)
                    new_cndtl.save()
    else:
        get_cn = CN.objects.get(docno=cn_no)
        get_cn_amount = get_cn.total
        # count = 0
        # count += int(box_qty > 0)
        # count += int(unit_qty > 0)
        save_cn = False
        
        enter_unit_discount = True

        if box_qty>0:
            filter_cndtl_box = CNDTL.objects.filter(headerautokey=get_cn,itemcode=item_code_instance, uom='BOX')
            smallest_qty = box_qty*box_rate
            smallest_unit_price = box_price/box_rate
            total_box_price = box_price * box_qty

            if not filter_cndtl_box:
                if discount_amount > 0.0:
                    enter_unit_discount = False
                    total_box_price = total_box_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=box_uom,useruom=box_uom,qty=box_qty,rate=box_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=box_price,subtotal=total_box_price,localsubtotal=total_box_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_box_price,goodsreturn=goods_return,taxableamt=total_box_price,localsubtotalextax=total_box_price,discountamt=discount_amount,discount=discount_amount,localtaxableamt=total_box_price,taxcurrencytaxableamt=total_box_price)
                    new_cndtl.save()

                   
                    previous_cn = CN.objects.get(docno=cn_no)
                    new_value = previous_cn.total + total_box_price

                    previous_cn.total = new_value
                    previous_cn.nettotal = new_value
                    previous_cn.localnettotal = new_value
                    previous_cn.analysisnettotal = new_value
                    previous_cn.localanalysisnettotal = new_value
                    previous_cn.totalextax = new_value
                    previous_cn.finaltotal = new_value
                    previous_cn.localtaxableamt = new_value
                    previous_cn.taxcurrencytaxableamt = new_value
                    previous_cn.save()
                else:
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=box_uom,useruom=box_uom,qty=box_qty,rate=box_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=box_price,subtotal=total_box_price,localsubtotal=total_box_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_box_price,goodsreturn=goods_return,taxableamt=total_box_price,localsubtotalextax=total_box_price,localtaxableamt=total_box_price,discount=0,discountamt=0,taxcurrencytaxableamt=total_box_price)
                    new_cndtl.save()

                    previous_cn = CN.objects.get(docno=cn_no)
                    new_value = previous_cn.total + total_box_price
                    previous_cn.total = new_value
                    previous_cn.nettotal = new_value
                    previous_cn.localnettotal = new_value
                    previous_cn.analysisnettotal = new_value
                    previous_cn.localanalysisnettotal = new_value
                    previous_cn.totalextax = new_value
                    previous_cn.finaltotal = new_value
                    previous_cn.localtaxableamt = new_value
                    previous_cn.taxcurrencytaxableamt = new_value
                    previous_cn.save()
            else:
                save_cn = True
                filter_cndtl_object = CNDTL.objects.get(headerautokey=get_cn,itemcode=item_code_instance,uom='BOX')
                # filter_cndtl_object.extradiscountamt = 0
                if filter_cndtl_object.discount != None:
                    previous_net_amount = filter_cndtl_object.subtotal - Decimal(float(filter_cndtl_object.discount)).quantize(Decimal('0.00'))
                else:
                    previous_net_amount = filter_cndtl_object.subtotal
                get_cn_amount = get_cn_amount - previous_net_amount 

                if discount_amount > 0.0:
                    enter_unit_discount = False
                    total_box_price = total_box_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    filter_cndtl_object.discount = discount_amount
                    filter_cndtl_object.discountamt = discount_amount
                    filter_cndtl_object.subtotal = total_box_price
                    filter_cndtl_object.localsubtotal = total_box_price
                    filter_cndtl_object.subtotalextax = total_box_price
                    filter_cndtl_object.taxableamt = total_box_price
                    filter_cndtl_object.localsubtotalextax = total_box_price
                    filter_cndtl_object.localtaxableamt = total_box_price
                    filter_cndtl_object.taxcurrencytaxableamt = total_box_price
                    filter_cndtl_object.save()

                    # previous_cn = CN.objects.get(docno=cn_no)
                    # new_value = previous_cn.total - discount_amount
                else:
                    filter_cndtl_object.discount = 0
                    filter_cndtl_object.discountamt = 0
                    filter_cndtl_object.subtotal = total_box_price
                    filter_cndtl_object.localsubtotal = total_box_price
                    filter_cndtl_object.subtotalextax = total_box_price
                    filter_cndtl_object.taxableamt = total_box_price
                    filter_cndtl_object.localsubtotalextax = total_box_price
                    filter_cndtl_object.localtaxableamt = total_box_price
                    filter_cndtl_object.taxcurrencytaxableamt = total_box_price
                    filter_cndtl_object.save()
            
        if unit_qty>0:
            filter_cndtl_unit = CNDTL.objects.filter(headerautokey=get_cn,itemcode=item_code_instance, uom='UNT')
            smallest_qty = unit_qty*unit_rate
            smallest_unit_price = unit_price/unit_rate
            total_unit_price = unit_price * unit_qty

            if not filter_cndtl_unit:
                if discount_amount > 0.0:
                    if not enter_unit_discount:
                        discount_amount = 0
                    
                    total_unit_price = total_unit_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit_qty,rate=unit_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_unit_price,goodsreturn=goods_return,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discountamt=discount_amount,discount=discount_amount,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price)
                    new_cndtl.save()

                    
                    previous_cn = CN.objects.get(docno=cn_no)
                    new_value = previous_cn.total + total_unit_price
                    previous_cn.total = new_value
                    previous_cn.nettotal = new_value
                    previous_cn.localnettotal = new_value
                    previous_cn.analysisnettotal = new_value
                    previous_cn.localanalysisnettotal = new_value
                    previous_cn.totalextax = new_value
                    previous_cn.finaltotal = new_value
                    previous_cn.localtaxableamt = new_value
                    previous_cn.taxcurrencytaxableamt = new_value
                    previous_cn.save()
                else:
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=unit_qty,rate=unit_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_unit_price,goodsreturn=goods_return,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price)
                    new_cndtl.save()

                    previous_cn = CN.objects.get(docno=cn_no)
                    new_value = previous_cn.total + total_unit_price
                    previous_cn.total = new_value
                    previous_cn.nettotal = new_value
                    previous_cn.localnettotal = new_value
                    previous_cn.analysisnettotal = new_value
                    previous_cn.localanalysisnettotal = new_value
                    previous_cn.totalextax = new_value
                    previous_cn.finaltotal = new_value
                    previous_cn.localtaxableamt = new_value
                    previous_cn.taxcurrencytaxableamt = new_value
                    previous_cn.save()
            else:
                save_cn = True
                filter_cndtl_object = CNDTL.objects.get(headerautokey=get_cn,itemcode=item_code_instance, uom='UNT')
                if filter_cndtl_object.discount != None:
                    previous_net_amount = filter_cndtl_object.subtotal - filter_cndtl_object.discount
                else:
                    previous_net_amount = filter_cndtl_object.subtotal
                get_cn_amount = get_cn_amount - previous_net_amount
                # filter_cndtl_object.extradiscountamt = 0

                if discount_amount > 0.0:
                    if not enter_unit_discount:
                        discount_amount = 0
                    total_unit_price = total_unit_price -  Decimal(discount_amount).quantize(Decimal('0.00'))
                    filter_cndtl_object.discount = discount_amount
                    filter_cndtl_object.discountamt = discount_amount
                    filter_cndtl_object.subtotal = total_unit_price
                    filter_cndtl_object.localsubtotal = total_unit_price
                    filter_cndtl_object.subtotalextax = total_unit_price
                    filter_cndtl_object.taxableamt = total_unit_price
                    filter_cndtl_object.localsubtotalextax = total_unit_price
                    filter_cndtl_object.localtaxableamt = total_unit_price
                    filter_cndtl_object.taxcurrencytaxableamt = total_unit_price
                    filter_cndtl_object.save()
                else:
                    filter_cndtl_object.discount = 0
                    filter_cndtl_object.discountamt = 0
                    filter_cndtl_object.subtotal = total_unit_price
                    filter_cndtl_object.localsubtotal = total_unit_price
                    filter_cndtl_object.subtotalextax = total_unit_price
                    filter_cndtl_object.taxableamt = total_unit_price
                    filter_cndtl_object.localsubtotalextax = total_unit_price
                    filter_cndtl_object.localtaxableamt = total_unit_price
                    filter_cndtl_object.taxcurrencytaxableamt = total_unit_price
                    filter_cndtl_object.save()

        if save_cn:
            get_cn_amount = get_cn_amount + Decimal(net_amount).quantize(Decimal('0.0000'))
            get_cn.total = get_cn_amount
            get_cn.nettotal = get_cn_amount
            get_cn.localnettotal = get_cn_amount
            get_cn.analysisnettotal = get_cn_amount
            get_cn.localanalysisnettotal = get_cn_amount
            get_cn.totalextax = get_cn_amount
            get_cn.finaltotal = get_cn_amount
            get_cn.localtaxableamt = get_cn_amount
            get_cn.taxcurrencytaxableamt = get_cn_amount
            get_cn.save()

        