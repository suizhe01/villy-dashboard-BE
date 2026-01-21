from debtor.models import Debtor
import datetime
from company.models import Company
from iv.models import IV
from ivdtl.models import IVDTL
from django.db import transaction
from branch.models import Branch
from terms.models import Terms
from itemuom.models import ItemUOM
from location.models import Location
from item.models import Item
from decimal import Decimal
from salesagent.models import SalesAgent

def create_dutchlady_iv_ivdtl(debtor_code, debtor_name,invoice_no,invoice_date,item_code,sales_agent,discount_amount,net_amount,box_qty,unit_qty,seq, box_price, unit_price,temporary_display_term,tempcompanyautokey,branchautokey, box_uom,box_rate,unit_uom,unit_rate,location,description,lorry_driver,udf_book2):
    is_debtor_exist = Debtor.objects.filter(accno=debtor_code).exists()
    is_salesagent_exist = SalesAgent.objects.filter(salesagent=sales_agent).exists()
    currency_code = 'MYR'
    allowexceedcreditlimit='T'
    discountpercent = 0
    datetimenow = datetime.datetime.now()
    lastmodifieduserid = 'ADMIN'
    hasbonuspoint='F'
    isgroupcompany = 'F'
    isactive = 'T'
    inclusivetax = 'F'
    filter_invoice_num = IV.objects.filter(docno=invoice_no).exists()
    currency_rate = 1
    post_to_stock = 'T'
    post_to_gl = 'T'
    transferable = 'T'
    print_out = 0
    cancelled = 'F'
    can_sync = 'F'
    last_update = 0
    reallocate_purchase_by_project = 'F'
    iv_description = 'INVOICE'
    main_item='T'
    item_code = Item.objects.get(itemcode=item_code)
    dtltype='N'
    add_to_sub_total = 'T'
    is_calc_bonus_point = 'T'
    to_tax_currency_rate = 1
    rounding_method = 4
    transfered_qty = 0
    box_price = Decimal(box_price).quantize(Decimal('0.00'))
    unit_price = Decimal(unit_price).quantize(Decimal('0.0000'))

    if not is_salesagent_exist:
        new_agent = SalesAgent(salesagent=sales_agent, lastupdate=0,isactive=1)
        new_agent.save()

    if not is_debtor_exist:
        new_debtor = Debtor(accno=debtor_code, companyname=debtor_name, displayterm=temporary_display_term, currencycode=currency_code,allowexceedcreditlimit=allowexceedcreditlimit,discountpercent=discountpercent,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid, hasbonuspoint=hasbonuspoint, isgroupcompany=isgroupcompany,isactive=isactive, lastupdate=0,inclusivetax=inclusivetax,roundingmethod=-1, companyautokey=tempcompanyautokey, selfbilledapprovalno=0)
        new_debtor.save()
             
    if not filter_invoice_num:
        with transaction.atomic():
            sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            filter_debtor = Debtor.objects.get(accno=debtor_code)
            debtor_name = filter_debtor.companyname
            new_iv = IV(udfbook = udf_book2,lorrydriver=lorry_driver,branchautokey=branchautokey,docno=invoice_no,docdate=invoice_date,displayterm=temporary_display_term,debtorcode=filter_debtor,debtorname=debtor_name,description=iv_description,total=net_amount,nettotal=net_amount,localnettotal=net_amount,analysisnettotal=net_amount,localanalysisnettotal=net_amount,finaltotal=net_amount,totalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount,salesagent=sales_agent,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_out,cancelled=cancelled,lastmodified=datetimenow,lastmodifieduserid=lastmodifieduserid,createdtimestamp=datetimenow,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            get_iv = IV.objects.filter(docno=invoice_no).first()
            
            enter_unit_discount = True

            if box_qty > 0:
                smallest_qty = box_qty*box_rate
                smallest_unit_price = box_price/box_rate
                total_box_price = box_price * box_qty
                if discount_amount > 0.0:
                    enter_unit_discount = False
                    # print('before',discount_amount,total_box_price)
                    total_box_price = total_box_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    # print('after', total_box_price)
                    new_iv_ivdtl = IVDTL(headerautokey=get_iv, seq=seq,mainitem=main_item,itemcode=item_code,location=location,description=description,uom=box_uom,useruom=box_uom,qty=box_qty,rate=box_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=box_price,subtotal=total_box_price,localsubtotal=total_box_price,transferable=transferable,printout=print_out,dtltype=dtltype,addtosubtotal=add_to_sub_total,iscalcbonuspoint=is_calc_bonus_point,subtotalextax=total_box_price,taxableamt=total_box_price,localsubtotalextax=total_box_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_box_price,taxcurrencytaxableamt=total_box_price,transferedqty=transfered_qty)
                    new_iv_ivdtl.save()
                else:
                    new_iv_ivdtl = IVDTL(headerautokey=get_iv, seq=seq,mainitem=main_item,itemcode=item_code,location=location,description=description,uom=box_uom,useruom=box_uom,qty=box_qty,rate=box_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=box_price,subtotal=total_box_price,localsubtotal=total_box_price,transferable=transferable,printout=print_out,dtltype=dtltype,addtosubtotal=add_to_sub_total,iscalcbonuspoint=is_calc_bonus_point,subtotalextax=total_box_price,taxableamt=total_box_price,localsubtotalextax=total_box_price,discount=0,discountamt=0,localtaxableamt=total_box_price,taxcurrencytaxableamt=total_box_price,transferedqty=transfered_qty)
                    new_iv_ivdtl.save()

            if unit_qty > 0:
                smallest_qty = unit_qty*unit_rate
                smallest_unit_price = unit_price/unit_rate
                total_unit_price = unit_price*unit_qty
                if discount_amount > 0.0:
                    if not enter_unit_discount:
                        discount_amount = 0
                    total_unit_price = total_unit_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    new_iv_ivdtl = IVDTL(headerautokey=get_iv, seq=seq,mainitem=main_item,itemcode=item_code,location=location,description=description,uom=unit_uom,useruom=unit_uom,qty=unit_qty,rate=unit_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,transferable=transferable,printout=print_out,dtltype=dtltype,addtosubtotal=add_to_sub_total,iscalcbonuspoint=is_calc_bonus_point,subtotalextax=total_unit_price,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price,transferedqty=transfered_qty)
                    new_iv_ivdtl.save()
                else:
                    new_iv_ivdtl = IVDTL(headerautokey=get_iv, seq=seq,mainitem=main_item,itemcode=item_code,location=location,description=description,uom=unit_uom,useruom=unit_uom,qty=unit_qty,rate=unit_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,transferable=transferable,printout=print_out,dtltype=dtltype,addtosubtotal=add_to_sub_total,iscalcbonuspoint=is_calc_bonus_point,subtotalextax=total_unit_price,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discount=0,discountamt=0,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price,transferedqty=transfered_qty)
                    new_iv_ivdtl.save()
    else:
        get_iv = IV.objects.get(docno=invoice_no)
        get_iv_amount = get_iv.total
        # count = 0
        # count += int(box_qty > 0)
        # count += int(unit_qty > 0)
        save_iv = False

        enter_unit_discount = True
        
        if box_qty>0:
            filter_iv_dtl_box = IVDTL.objects.filter(headerautokey=get_iv,itemcode=item_code, uom="BOX")
            smallest_qty = box_qty*box_rate
            smallest_unit_price = box_price/box_rate
            total_box_price = box_price * box_qty

            if not filter_iv_dtl_box:
                if discount_amount > 0.0:
                    enter_unit_discount = False
                    total_box_price = total_box_price -  Decimal(discount_amount).quantize(Decimal('0.00'))

                    new_iv_ivdtl = IVDTL(headerautokey=get_iv, seq=seq,mainitem=main_item,itemcode=item_code,location=location,description=description,uom=box_uom,useruom=box_uom,qty=box_qty,rate=box_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=box_price,subtotal=total_box_price,localsubtotal=total_box_price,transferable=transferable,printout=print_out,dtltype=dtltype,addtosubtotal=add_to_sub_total,iscalcbonuspoint=is_calc_bonus_point,subtotalextax=total_box_price,taxableamt=total_box_price,localsubtotalextax=total_box_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_box_price,taxcurrencytaxableamt=total_box_price,transferedqty=transfered_qty)
                    new_iv_ivdtl.save()

                    
                    previous_iv = IV.objects.get(docno=invoice_no)
                    new_value = previous_iv.total + total_box_price
                    previous_iv.total = new_value
                    previous_iv.nettotal = new_value
                    previous_iv.localnettotal = new_value
                    previous_iv.analysisnettotal = new_value
                    previous_iv.localanalysisnettotal = new_value
                    previous_iv.finaltotal = new_value
                    previous_iv.totalextax = new_value
                    previous_iv.localtaxableamt = new_value
                    previous_iv.taxcurrencytaxableamt = new_value
                    previous_iv.save()
                else:
                    new_iv_ivdtl = IVDTL(headerautokey=get_iv, seq=seq,mainitem=main_item,itemcode=item_code,location=location,description=description,uom=box_uom,useruom=box_uom,qty=box_qty,rate=box_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=box_price,subtotal=total_box_price,localsubtotal=total_box_price,transferable=transferable,printout=print_out,dtltype=dtltype,addtosubtotal=add_to_sub_total,iscalcbonuspoint=is_calc_bonus_point,subtotalextax=total_box_price,taxableamt=total_box_price,localsubtotalextax=total_box_price,discount=0,discountamt=0,localtaxableamt=total_box_price,taxcurrencytaxableamt=total_box_price,transferedqty=transfered_qty)
                    new_iv_ivdtl.save()

                    previous_iv = IV.objects.get(docno=invoice_no)
                    new_value = previous_iv.total + total_box_price
                    previous_iv.total = new_value
                    previous_iv.nettotal = new_value
                    previous_iv.localnettotal = new_value
                    previous_iv.analysisnettotal = new_value
                    previous_iv.localanalysisnettotal = new_value
                    previous_iv.finaltotal = new_value
                    previous_iv.totalextax = new_value
                    previous_iv.localtaxableamt = new_value
                    previous_iv.taxcurrencytaxableamt = new_value
                    previous_iv.save()
            else:
                save_iv = True
                filter_iv_ivdtl_box_object = IVDTL.objects.get(headerautokey=get_iv,itemcode=item_code, uom="BOX")
                if filter_iv_ivdtl_box_object.discount != None:
                    previous_net_amount = filter_iv_ivdtl_box_object.subtotal - Decimal(float(filter_iv_ivdtl_box_object.discount)).quantize(Decimal('0.00'))
                else:
                    previous_net_amount = filter_iv_ivdtl_box_object.subtotal
                get_iv_amount = get_iv_amount - previous_net_amount

                if discount_amount > 0.0:
                    enter_unit_discount = False
                    total_box_price = total_box_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    filter_iv_ivdtl_box_object.discount = discount_amount
                    filter_iv_ivdtl_box_object.discountamt = discount_amount
                    filter_iv_ivdtl_box_object.subtotal = total_box_price
                    filter_iv_ivdtl_box_object.localsubtotal = total_box_price
                    filter_iv_ivdtl_box_object.subtotalextax = total_box_price
                    filter_iv_ivdtl_box_object.taxableamt = total_box_price
                    filter_iv_ivdtl_box_object.localsubtotalextax = total_box_price
                    filter_iv_ivdtl_box_object.localtaxableamt = total_box_price
                    filter_iv_ivdtl_box_object.taxcurrencytaxableamt = total_box_price
                    filter_iv_ivdtl_box_object.smallestqty = smallest_qty
                    filter_iv_ivdtl_box_object.smallestunitprice = smallest_unit_price
                    filter_iv_ivdtl_box_object.qty = box_qty
                    filter_iv_ivdtl_box_object.unitprice = box_price
                    filter_iv_ivdtl_box_object.save()
                else:
                    filter_iv_ivdtl_box_object.discount = 0
                    filter_iv_ivdtl_box_object.discountamt = 0
                    filter_iv_ivdtl_box_object.subtotal = total_box_price
                    filter_iv_ivdtl_box_object.localsubtotal = total_box_price
                    filter_iv_ivdtl_box_object.subtotalextax = total_box_price
                    filter_iv_ivdtl_box_object.taxableamt = total_box_price
                    filter_iv_ivdtl_box_object.localsubtotalextax = total_box_price
                    filter_iv_ivdtl_box_object.localtaxableamt = total_box_price
                    filter_iv_ivdtl_box_object.taxcurrencytaxableamt = total_box_price
                    filter_iv_ivdtl_box_object.smallestqty = smallest_qty
                    filter_iv_ivdtl_box_object.smallestunitprice = smallest_unit_price
                    filter_iv_ivdtl_box_object.qty = box_qty
                    filter_iv_ivdtl_box_object.unitprice = box_price
                    filter_iv_ivdtl_box_object.save()

        if unit_qty>0:
            filter_iv_dtl_unit = IVDTL.objects.filter(headerautokey=get_iv,itemcode=item_code, uom="unit")
            smallest_qty = unit_qty*unit_rate
            smallest_unit_price = unit_price/unit_rate
            total_unit_price = unit_price*unit_qty

            if not filter_iv_dtl_unit:
                if discount_amount > 0.0:
                    if not enter_unit_discount:
                        discount_amount = 0
                    
                    total_unit_price = total_unit_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    new_iv_ivdtl = IVDTL(headerautokey=get_iv, seq=seq,mainitem=main_item,itemcode=item_code,location=location,description=description,uom=unit_uom,useruom=unit_uom,qty=unit_qty,rate=unit_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,transferable=transferable,printout=print_out,dtltype=dtltype,addtosubtotal=add_to_sub_total,iscalcbonuspoint=is_calc_bonus_point,subtotalextax=total_unit_price,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discount=discount_amount,discountamt=discount_amount,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price,transferedqty=transfered_qty)
                    new_iv_ivdtl.save()

                    
                    previous_iv = IV.objects.get(docno=invoice_no)
                    new_value = previous_iv.total + total_unit_price
                    previous_iv.total = new_value
                    previous_iv.nettotal = new_value
                    previous_iv.localnettotal = new_value
                    previous_iv.analysisnettotal = new_value
                    previous_iv.localanalysisnettotal = new_value
                    previous_iv.finaltotal = new_value
                    previous_iv.totalextax = new_value
                    previous_iv.localtaxableamt = new_value
                    previous_iv.taxcurrencytaxableamt = new_value
                    previous_iv.save()
                else:
                    new_iv_ivdtl = IVDTL(headerautokey=get_iv, seq=seq,mainitem=main_item,itemcode=item_code,location=location,description=description,uom=unit_uom,useruom=unit_uom,qty=unit_qty,rate=unit_rate,smallestqty=smallest_qty,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=total_unit_price,localsubtotal=total_unit_price,transferable=transferable,printout=print_out,dtltype=dtltype,addtosubtotal=add_to_sub_total,iscalcbonuspoint=is_calc_bonus_point,subtotalextax=total_unit_price,taxableamt=total_unit_price,localsubtotalextax=total_unit_price,discount=0,discountamt=0,localtaxableamt=total_unit_price,taxcurrencytaxableamt=total_unit_price,transferedqty=transfered_qty)
                    new_iv_ivdtl.save()

                    previous_iv = IV.objects.get(docno=invoice_no)
                    new_value = previous_iv.total + total_unit_price
                    previous_iv.total = new_value
                    previous_iv.nettotal = new_value
                    previous_iv.localnettotal = new_value
                    previous_iv.analysisnettotal = new_value
                    previous_iv.localanalysisnettotal = new_value
                    previous_iv.finaltotal = new_value
                    previous_iv.totalextax = new_value
                    previous_iv.localtaxableamt = new_value
                    previous_iv.taxcurrencytaxableamt = new_value
                    previous_iv.save()
            else:
                save_iv = True
                
                # get_iv_amount = get_iv_object.total
                filter_iv_ivdtl_unit_object = IVDTL.objects.get(headerautokey=get_iv,itemcode=item_code, uom="unit")
                if filter_iv_ivdtl_unit_object.discount != None:
                    previous_net_amount = filter_iv_ivdtl_unit_object.subtotal - Decimal(float(filter_iv_ivdtl_unit_object.discount)).quantize(Decimal('0.00'))
                else:
                    previous_net_amount = filter_iv_ivdtl_unit_object.subtotal
                get_iv_amount = get_iv_amount - previous_net_amount

                if discount_amount > 0.0:
                    if not enter_unit_discount:
                        discount_amount = 0
                    total_unit_price = total_unit_price - Decimal(discount_amount).quantize(Decimal('0.00'))
                    filter_iv_ivdtl_unit_object.discount = discount_amount
                    filter_iv_ivdtl_unit_object.discountamt = discount_amount
                    filter_iv_ivdtl_unit_object.subtotal = total_unit_price
                    filter_iv_ivdtl_unit_object.localsubtotal = total_unit_price
                    filter_iv_ivdtl_unit_object.subtotalextax = total_unit_price
                    filter_iv_ivdtl_unit_object.taxableamt = total_unit_price
                    filter_iv_ivdtl_unit_object.localsubtotalextax = total_unit_price
                    filter_iv_ivdtl_unit_object.localtaxableamt = total_unit_price
                    filter_iv_ivdtl_unit_object.taxcurrencytaxableamt = total_unit_price
                    filter_iv_ivdtl_unit_object.smallestqty = smallest_qty
                    filter_iv_ivdtl_unit_object.smallestunitprice = smallest_unit_price
                    filter_iv_ivdtl_unit_object.qty = unit_qty
                    filter_iv_ivdtl_unit_object.unitprice = unit_price
                    filter_iv_ivdtl_unit_object.save()
                else:
                    filter_iv_ivdtl_unit_object.discountamt = 0
                    filter_iv_ivdtl_unit_object.discount = 0
                    filter_iv_ivdtl_unit_object.subtotal = total_unit_price
                    filter_iv_ivdtl_unit_object.localsubtotal = total_unit_price
                    filter_iv_ivdtl_unit_object.subtotalextax = total_unit_price
                    filter_iv_ivdtl_unit_object.taxableamt = total_unit_price
                    filter_iv_ivdtl_unit_object.localsubtotalextax = total_unit_price
                    filter_iv_ivdtl_unit_object.localtaxableamt = total_unit_price
                    filter_iv_ivdtl_unit_object.taxcurrencytaxableamt = total_unit_price
                    filter_iv_ivdtl_unit_object.smallestqty = smallest_qty
                    filter_iv_ivdtl_unit_object.smallestunitprice = smallest_unit_price
                    filter_iv_ivdtl_unit_object.qty = unit_qty
                    filter_iv_ivdtl_unit_object.unitprice = unit_price
                    filter_iv_ivdtl_unit_object.save()

        if save_iv:
            get_iv_amount = get_iv_amount + Decimal(net_amount).quantize(Decimal('0.00'))
            get_iv.total = get_iv_amount
            get_iv.nettotal = get_iv_amount
            get_iv.localnettotal = get_iv_amount
            get_iv.analysisnettotal = get_iv_amount
            get_iv.localanalysisnettotal = get_iv_amount
            get_iv.finaltotal = get_iv_amount
            get_iv.totalextax = get_iv_amount
            get_iv.localtaxableamt = get_iv_amount
            get_iv.taxcurrencytaxableamt = get_iv_amount
            get_iv.save()

