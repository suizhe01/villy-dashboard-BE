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

def create_redbull_cn_cndtl(cn_no,cn_date,debtor_code,debtor_name,invoice_no,net_amount,reason_description,item_code,qty_in_ctn,qty_in_otr,qty_in_unit,discount_amount,batch_no,seq,ctn_price,otr_price,unit_price,temporary_display_term,tempcompanyautokey,branchautokey,location_instance,ctn_rate,ctn_uom,otr_rate,otr_uom,unit_rate,unit_uom, description,sales_agent):

    qty_in_ctn = int(qty_in_ctn)
    qty_in_otr = int(qty_in_otr)
    qty_in_unit = int(qty_in_unit)
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
            new_cn = CN(lorrydriver='NA',salesagent=sales_agent,branchautokey=branchautokey,docno=cn_no,docdate=cn_date,debtorcode=filter_debtor,debtorname=debtor_name,ourinvoiceno=invoice_no,description=iv_description,totaxcurrencyrate=1,displayterm=temporary_display_term,total=net_amount,currencycode=currency_code,currencyrate=currency_rate,nettotal=net_amount,localnettotal=net_amount,analysisnettotal=net_amount,localanalysisnettotal=net_amount,posttostock=post_to_stock,posttogl=post_to_gl,printcount=print_out,cancelled=cancelled,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid,createdtimestamp=datetimenow,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=0,calcdiscountonunitprice=calculate_discount_on_unit_price,totalextax=net_amount,reason=reason_description,inclusivetax=inclusivetax,isroundadj=isroundadj,finaltotal=net_amount,roundingmethod=rounding_method,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
            new_cn.save()

            get_cn = CN.objects.get(docno=cn_no)
            enter_unit_discount = True

            if qty_in_ctn >0:
                smallestqty = qty_in_ctn*ctn_rate
                smallest_unit_price = ctn_price/ctn_rate
                total_ctn_price = ctn_price * qty_in_ctn

                if discount_amount>0:
                    enter_unit_discount = False
                    total_ctn_price = Decimal(total_ctn_price).quantize(Decimal('0.00')) - Decimal(discount_amount).quantize(Decimal('0.00'))
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=ctn_uom,useruom=ctn_uom,qty=qty_in_ctn,rate=ctn_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=ctn_price,subtotal=total_ctn_price,localsubtotal=total_ctn_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_ctn_price,goodsreturn=goods_return,taxableamt=total_ctn_price,localsubtotalextax=total_ctn_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_ctn_price,taxcurrencytaxableamt=total_ctn_price, batchno=batch_no)
                    new_cndtl.save()
                else:
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=ctn_uom,useruom=ctn_uom,qty=qty_in_ctn,rate=ctn_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=ctn_price,subtotal=total_ctn_price,localsubtotal=total_ctn_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_ctn_price,goodsreturn=goods_return,taxableamt=total_ctn_price,localsubtotalextax=total_ctn_price,localtaxableamt=total_ctn_price,taxcurrencytaxableamt=total_ctn_price, batchno=batch_no)
                    new_cndtl.save()

            if qty_in_otr >0:
                smallestqty = qty_in_otr*otr_rate
                smallest_unit_price = otr_price/otr_rate
                total_otr_price = otr_price * qty_in_otr

                if discount_amount>0:
                    if not enter_unit_discount:
                        discount_amount = 0
                    else:
                        enter_unit_discount = False
                    total_otr_price = total_otr_price - discount_amount
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=otr_uom,useruom=otr_uom,qty=qty_in_otr,rate=otr_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=otr_price,subtotal=total_otr_price,localsubtotal=total_otr_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_otr_price,goodsreturn=goods_return,taxableamt=total_otr_price,localsubtotalextax=total_otr_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_otr_price,taxcurrencytaxableamt=total_otr_price, batchno=batch_no)
                    new_cndtl.save()
                else:
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=otr_uom,useruom=otr_uom,qty=qty_in_otr,rate=otr_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=otr_price,subtotal=total_otr_price,localsubtotal=total_otr_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_otr_price,goodsreturn=goods_return,taxableamt=total_otr_price,localsubtotalextax=total_otr_price,localtaxableamt=total_otr_price,taxcurrencytaxableamt=total_otr_price, batchno=batch_no)
                    new_cndtl.save()

            if qty_in_unit >0:
                smallestqty = qty_in_unit*unit_rate
                smallest_unit_price = unit_price/unit_rate
                total_unit_price = unit_price * qty_in_unit
                
                if discount_amount>0:
                    if not enter_unit_discount:
                        discount_amount = 0
                    total_unit_price = total_unit_price - discount_amount
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=qty_in_unit,rate=unit_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_unit_price,goodsreturn=goods_return,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price, batchno=batch_no)
                    new_cndtl.save()
                else:
                    new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=qty_in_unit,rate=unit_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_unit_price,goodsreturn=goods_return,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price, batchno=batch_no)
                    new_cndtl.save()
    else:
        get_cn = CN.objects.get(docno=cn_no)
        get_cn_amount = get_cn.total
        save_cn = False
        enter_unit_discount = True

        if qty_in_ctn >0:
            # filter_cndtl_ctn = CNDTL.objects.filter(headerautokey=get_cn,itemcode=item_code_instance,uom='CTN',subtotal__gt=0)
            smallestqty = qty_in_ctn*ctn_rate
            smallest_unit_price = ctn_price/ctn_rate
            total_ctn_price = ctn_price * qty_in_ctn

            # if not filter_cndtl_ctn:
            if discount_amount>0.0:
                enter_unit_discount = False
                total_ctn_price = Decimal(total_ctn_price).quantize(Decimal('0.00')) - Decimal(discount_amount).quantize(Decimal('0.00'))
                new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=ctn_uom,useruom=ctn_uom,qty=qty_in_ctn,rate=ctn_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=ctn_price,subtotal=total_ctn_price,localsubtotal=total_ctn_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_ctn_price,goodsreturn=goods_return,taxableamt=total_ctn_price,localsubtotalextax=total_ctn_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_ctn_price,taxcurrencytaxableamt=total_ctn_price, batchno=batch_no)
                new_cndtl.save()

                previous_cn = CN.objects.get(docno=cn_no)
                new_value = previous_cn.total + total_ctn_price

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
                new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=ctn_uom,useruom=ctn_uom,qty=qty_in_ctn,rate=ctn_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=ctn_price,subtotal=total_ctn_price,localsubtotal=total_ctn_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_ctn_price,goodsreturn=goods_return,taxableamt=total_ctn_price,localsubtotalextax=total_ctn_price,localtaxableamt=total_ctn_price,taxcurrencytaxableamt=total_ctn_price, batchno=batch_no)
                new_cndtl.save()

                previous_cn = CN.objects.get(docno=cn_no)
                new_value = previous_cn.total + Decimal(total_ctn_price).quantize(Decimal('0.00'))
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
            # else:
            #     save_cn = True
            #     filter_cndtl_object = CNDTL.objects.get(headerautokey=get_cn,itemcode=item_code_instance,uom='CTN',subtotal__gt=0)

            #     if filter_cndtl_object.discount != None:
            #         previous_net_amount = filter_cndtl_object.subtotal - Decimal(filter_cndtl_object.discount).quantize(Decimal('0.00'))
            #     else:
            #         previous_net_amount = filter_cndtl_object.subtotal
            #     get_cn_amount = get_cn_amount - previous_net_amount

            #     if discount_amount > 0.0:
            #         enter_unit_discount = False
            #         total_ctn_price = Decimal(total_ctn_price).quantize(Decimal('0.00')) - Decimal(discount_amount).quantize(Decimal('0.00'))
            #         filter_cndtl_object.discount = discount_amount
            #         filter_cndtl_object.discountamt = discount_amount
            #         filter_cndtl_object.subtotal = total_ctn_price
            #         filter_cndtl_object.localsubtotal = total_ctn_price
            #         filter_cndtl_object.subtotalextax = total_ctn_price
            #         filter_cndtl_object.taxableamt = total_ctn_price
            #         filter_cndtl_object.localsubtotalextax = total_ctn_price
            #         filter_cndtl_object.localtaxableamt = total_ctn_price
            #         filter_cndtl_object.taxcurrencytaxableamt = total_ctn_price
            #         filter_cndtl_object.save()
            #     else:
            #         filter_cndtl_object.discountamt = 0
            #         filter_cndtl_object.discount = 0
            #         filter_cndtl_object.subtotal = total_ctn_price
            #         filter_cndtl_object.localsubtotal = total_ctn_price
            #         filter_cndtl_object.subtotalextax = total_ctn_price
            #         filter_cndtl_object.taxableamt = total_ctn_price
            #         filter_cndtl_object.localsubtotalextax = total_ctn_price
            #         filter_cndtl_object.localtaxableamt = total_ctn_price
            #         filter_cndtl_object.taxcurrencytaxableamt = total_ctn_price
            #         filter_cndtl_object.save()

        if qty_in_otr >0:
            filter_cndtl_otr = CNDTL.objects.filter(headerautokey=get_cn,itemcode=item_code_instance, uom='OTR',subtotal__gt=0)
            smallestqty = qty_in_otr*otr_rate
            smallest_unit_price = otr_price/otr_rate
            total_otr_price = otr_price * qty_in_otr

            # if not filter_cndtl_otr:
            if discount_amount>0.0:
                if not enter_unit_discount:
                    discount_amount = 0
                else:
                    enter_unit_discount = False

                total_otr_price =  Decimal(total_otr_price).quantize(Decimal('0.00')) - Decimal(discount_amount).quantize(Decimal('0.00'))
                new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=otr_uom,useruom=otr_uom,qty=qty_in_otr,rate=otr_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=otr_price,subtotal=total_otr_price,localsubtotal=total_otr_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_otr_price,goodsreturn=goods_return,taxableamt=total_otr_price,localsubtotalextax=total_otr_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_otr_price,taxcurrencytaxableamt=total_otr_price, batchno=batch_no)
                new_cndtl.save()

                previous_cn = CN.objects.get(docno=cn_no)
                new_value = previous_cn.total + total_otr_price
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
                new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=otr_uom,useruom=otr_uom,qty=qty_in_otr,rate=otr_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=otr_price,subtotal=total_otr_price,localsubtotal=total_otr_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_otr_price,goodsreturn=goods_return,taxableamt=total_otr_price,localsubtotalextax=total_otr_price,localtaxableamt=total_otr_price,taxcurrencytaxableamt=total_otr_price, batchno=batch_no)
                new_cndtl.save()

                previous_cn = CN.objects.get(docno=cn_no)
                new_value = previous_cn.total +  Decimal(total_otr_price).quantize(Decimal('0.00'))
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

            # else:
            #     save_cn = True
            #     filter_cndtl_object = CNDTL.objects.get(headerautokey=get_cn,itemcode=item_code_instance, uom='OTR',subtotal__gt=0)
            #     if filter_cndtl_object.discount != None:
            #         previous_net_amount = filter_cndtl_object.subtotal - Decimal(filter_cndtl_object.discount).quantize(Decimal('0.00'))
            #     else:
            #         previous_net_amount = filter_cndtl_object.subtotal
            #     get_cn_amount = get_cn_amount - previous_net_amount

            #     if discount_amount > 0.0:
            #         if not enter_unit_discount:
            #             discount_amount = 0
            #         else:
            #             enter_unit_discount = False

            #         total_otr_price = Decimal(total_otr_price).quantize(Decimal('0.00')) - Decimal(discount_amount).quantize(Decimal('0.00'))
            #         filter_cndtl_object.discount = discount_amount
            #         filter_cndtl_object.discountamt = discount_amount
            #         filter_cndtl_object.subtotal = total_otr_price
            #         filter_cndtl_object.localsubtotal = total_otr_price
            #         filter_cndtl_object.subtotalextax = total_otr_price
            #         filter_cndtl_object.taxableamt = total_otr_price
            #         filter_cndtl_object.localsubtotalextax = total_otr_price
            #         filter_cndtl_object.localtaxableamt = total_otr_price
            #         filter_cndtl_object.taxcurrencytaxableamt = total_otr_price
            #         filter_cndtl_object.save()
            #     else:
            #         filter_cndtl_object.discount = 0
            #         filter_cndtl_object.discountamt = 0
            #         filter_cndtl_object.subtotal = total_otr_price
            #         filter_cndtl_object.localsubtotal = total_otr_price
            #         filter_cndtl_object.subtotalextax = total_otr_price
            #         filter_cndtl_object.taxableamt = total_otr_price
            #         filter_cndtl_object.localsubtotalextax = total_otr_price
            #         filter_cndtl_object.localtaxableamt = total_otr_price
            #         filter_cndtl_object.taxcurrencytaxableamt = total_otr_price
            #         filter_cndtl_object.save()

        if qty_in_unit >0:
            filter_cndtl_unit = CNDTL.objects.filter(headerautokey=get_cn,itemcode=item_code_instance, uom='UNT', subtotal__gt=0)
            smallestqty = qty_in_unit*unit_rate
            smallest_unit_price = unit_price/unit_rate
            total_unit_price =unit_price * qty_in_unit

            # if not filter_cndtl_unit:
            if discount_amount>0.0:
                if not enter_unit_discount:
                    discount_amount = 0
                total_unit_price = Decimal(total_unit_price).quantize(Decimal('0.00')) - Decimal(discount_amount).quantize(Decimal('0.00'))
                new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=qty_in_unit,rate=unit_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_unit_price,goodsreturn=goods_return,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price, batchno=batch_no)
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
                new_cndtl = CNDTL(headerautokey=get_cn,seq=seq,mainitem=mainitem,itemcode=item_code_instance,location=location_instance,description=description,uom=unit_uom,useruom=unit_uom,qty=qty_in_unit,rate=unit_rate,smallestqty=smallestqty,smallestunitprice=smallest_unit_price, unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,printout=print_out,addtosubtotal=add_to_subtotal,iscalcbonuspoint=is_calculate_bonus_point,subtotalextax=total_unit_price,goodsreturn=goods_return,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price, batchno=batch_no)
                new_cndtl.save()

                previous_cn = CN.objects.get(docno=cn_no)
                new_value = previous_cn.total +  Decimal(total_unit_price).quantize(Decimal('0.00'))
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
            # else:
            #     save_cn = True
            #     filter_cndtl_object = CNDTL.objects.get(headerautokey=get_cn,itemcode=item_code_instance, uom='UNT', subtotal__gt=0)
            #     if filter_cndtl_object.discount != None:
            #         previous_net_amount = filter_cndtl_object.subtotal - Decimal(filter_cndtl_object.discount).quantize(Decimal('0.00'))
            #     else:
            #         previous_net_amount = filter_cndtl_object.subtotal
            #     get_cn_amount = get_cn_amount - previous_net_amount
            #     total_unit_price =unit_price * qty_in_unit

            #     if discount_amount > 0.0:
            #         if not enter_unit_discount:
            #             discount_amount = 0
            #         total_unit_price = Decimal(total_unit_price).quantize(Decimal('0.00')) - Decimal(discount_amount).quantize(Decimal('0.00'))
            #         filter_cndtl_object.discount = discount_amount
            #         filter_cndtl_object.discountamt = discount_amount
            #         filter_cndtl_object.subtotal = total_unit_price
            #         filter_cndtl_object.localsubtotal = total_unit_price
            #         filter_cndtl_object.subtotalextax = total_unit_price
            #         filter_cndtl_object.taxableamt = total_unit_price
            #         filter_cndtl_object.localsubtotalextax = total_unit_price
            #         filter_cndtl_object.localtaxableamt = total_unit_price
            #         filter_cndtl_object.taxcurrencytaxableamt = total_unit_price
            #         filter_cndtl_object.save()
            #     else:
            #         filter_cndtl_object.discount = 0
            #         filter_cndtl_object.discountamt = 0
            #         filter_cndtl_object.subtotal = total_unit_price
            #         filter_cndtl_object.localsubtotal = total_unit_price
            #         filter_cndtl_object.subtotalextax = total_unit_price
            #         filter_cndtl_object.taxableamt = total_unit_price
            #         filter_cndtl_object.localsubtotalextax = total_unit_price
            #         filter_cndtl_object.localtaxableamt = total_unit_price
            #         filter_cndtl_object.taxcurrencytaxableamt = total_unit_price
            #         filter_cndtl_object.save()

        # if save_cn:
        #     get_cn_amount = get_cn_amount + Decimal(net_amount).quantize(Decimal('0.00'))
        #     get_cn.total = get_cn_amount
        #     get_cn.nettotal = get_cn_amount
        #     get_cn.localnettotal = get_cn_amount
        #     get_cn.analysisnettotal = get_cn_amount
        #     get_cn.localanalysisnettotal = get_cn_amount
        #     get_cn.totalextax = get_cn_amount
        #     get_cn.finaltotal = get_cn_amount
        #     get_cn.localtaxableamt = get_cn_amount
        #     get_cn.taxcurrencytaxableamt = get_cn_amount
        #     get_cn.save()
