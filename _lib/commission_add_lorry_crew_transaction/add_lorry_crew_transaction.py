from lorry.models import Lorry
from crew.models import Crew
from transaction.models import Transaction
from transactiondtl.models import TransactionDtl
from itemclass.models import ItemClass
from iv.models import IV
from ivdtl.models import IVDTL
from item.models import Item

from acitem.models import AcItem
from acitemuom.models import AcItemUOM
from acsalesagent.models import AcSalesAgent
from acterms.models import AcTerms
from acdebtor.models import AcDebtor
from aciv.models import AcIV
from acivdtl.models import AcIVDTL

from item.models import Item
from itemuom.models import ItemUOM
from salesagent.models import SalesAgent
from terms.models import Terms
from debtor.models import Debtor
from iv.models import IV
from ivdtl.models import IVDTL
from branch.models import Branch
from datetime import datetime
from _lib import panda
from django.db import transaction
from location.models import Location
from rest_framework import status
from django.http import JsonResponse
from itertools import chain
from crewdtl.models import Crewdtl
from commissionitemclass.models import CommissionItemClass
from _lib.panda import panda_uuid
from django.db.models import Q

def import_item_from_autocount(tempcompanyautokey):
    autocount_server_item = AcItem.objects.using('windows_server').only('itemcode', 'itemgroup', 'description', 'itemclass','lastmodified','isactive','description').iterator()
    autocount_server_book2_item = AcItem.objects.using('windows_server_book2').only('itemcode', 'itemgroup', 'description', 'itemclass','lastmodified','isactive','description').iterator()
    autocount_server_book3_item = AcItem.objects.using('windows_server_book3').only('itemcode', 'itemgroup', 'description', 'itemclass','lastmodified','isactive','description').iterator()
    # Combine iterators
    combined_item_iterator = list(chain(autocount_server_item, autocount_server_book2_item,autocount_server_book3_item))

    ubuntu_server_items = Item.objects.values_list('itemcode', 'lastmodified','itemclass')
    ubuntu_server_itemcode = {item[0]: (item[1], item[2]) for item in ubuntu_server_items}
    new_items_to_create = []
    items_to_update = []

    for item in combined_item_iterator:
        last_modified = item.lastmodified
        item_code = item.itemcode
        item_brand = item.itemgroup or 'NA'
        description = item.description
        mainsupplier = item.itemgroup or 'NA'
        item_group = item.itemgroup or 'NA'
        item_class = item.itemclass
        is_active = item.isactive   
        
        if item_code not in ubuntu_server_itemcode and not any(existing_item.itemcode == item_code for existing_item in new_items_to_create):
            # print(new_items_to_create)
            save_new_item = Item(autokey=panda.panda_uuid(),itemgroup=item_group,itembrand=item_brand,itemcode=item_code,itemclass=item_class,description=description,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=last_modified,lastupdate=0)
            save_new_item.save()
            # different_itemclass_all.append(item_code)
            new_items_to_create.append(save_new_item)
        else:
            # # If the item exists in the ubuntu_server database, update the itemclass
            
            if (is_active == 'T') and not any(existing_item.itemcode == item_code for existing_item in new_items_to_create):
                ubuntu_last_modified, ubuntu_itemclass = ubuntu_server_itemcode[item_code]
                # if item_class == 'BARBGC0025011':
                #     print(item_class, ubuntu_itemclass)
                if (last_modified != ubuntu_last_modified) & (item_class != ubuntu_itemclass) & (item_class!=None):
                    items_to_update.append((item_code, item_class, last_modified))

    with transaction.atomic():

        # Bulk update itemclass for existing items
        for item_code, item_class, last_modified in items_to_update:
            Item.objects.filter(itemcode=item_code).update(itemclass=item_class, lastmodified=last_modified)

def import_itemuom_from_autocount(tempcompanyautokey):
    # Fetch all ItemUOMs from both databases

    filter_ubuntu_uom = ItemUOM.objects.filter(udfcalrate__gt=0)
    if filter_ubuntu_uom:
        # ubuntu_server_item_udf = {(item.itemcode.itemcode, item.uom): (item.udfcalmethod, item.udfcalrate) for item in filter_ubuntu_uom}
        # print(ubuntu_server_item_udf)
        for uom in filter_ubuntu_uom:
            udf_calmethod = uom.udfcalmethod
            udf_calrate = uom.udfcalrate
            item_code = uom.itemcode.itemcode
            uom = uom.uom

            filter_book1_uom = AcItemUOM.objects.using('windows_server').filter(itemcode=item_code,uom=uom).first()
            filter_book2_uom = AcItemUOM.objects.using('windows_server_book2').filter(itemcode=item_code,uom=uom).first()
            filter_book3_uom = AcItemUOM.objects.using('windows_server_book3').filter(itemcode=item_code,uom=uom).first()
            
            if filter_book1_uom:
                if (udf_calmethod!= filter_book1_uom.udfcalmethod) or (udf_calrate!=filter_book1_uom.udfcalrate):
                    update = ItemUOM.objects.get(itemcode=item_code,uom=uom)
                    update.udfcalmethod = filter_book1_uom.udfcalmethod
                    update.udfcalrate = filter_book1_uom.udfcalrate
                    update.save()

            if filter_book2_uom:
                if (udf_calmethod!= filter_book2_uom.udfcalmethod) or (udf_calrate!=filter_book2_uom.udfcalrate):
                    update = ItemUOM.objects.get(itemcode=item_code,uom=uom)
                    update.udfcalmethod = filter_book2_uom.udfcalmethod
                    update.udfcalrate = filter_book2_uom.udfcalrate
                    update.save()

            if filter_book3_uom:
                if (udf_calmethod!= filter_book3_uom.udfcalmethod) or (udf_calrate!=filter_book3_uom.udfcalrate):
                    update = ItemUOM.objects.get(itemcode=item_code,uom=uom)
                    update.udfcalmethod = filter_book3_uom.udfcalmethod
                    update.udfcalrate = filter_book3_uom.udfcalrate
                    update.save()

    filter_book3_uom = AcItemUOM.objects.using('windows_server_book2').filter(udfcalrate__gt=0)
    if filter_book3_uom:
        for uom in filter_book3_uom:
            udf_calmethod = uom.udfcalmethod
            udf_calrate = uom.udfcalrate
            item_code = uom.itemcode
            uom = uom.uom

            filter_ubuntu_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
            if filter_ubuntu_uom:
                if (udf_calmethod!= filter_ubuntu_uom.udfcalmethod) or (udf_calrate!=filter_ubuntu_uom.udfcalrate):
                    update = ItemUOM.objects.get(itemcode=item_code,uom=uom)
                    update.udfcalmethod = udf_calmethod
                    update.udfcalrate = udf_calrate
                    update.save()

    filter_book2_uom = AcItemUOM.objects.using('windows_server_book2').filter(udfcalrate__gt=0)
    if filter_book2_uom:
        for uom in filter_book2_uom:
            udf_calmethod = uom.udfcalmethod
            udf_calrate = uom.udfcalrate
            item_code = uom.itemcode
            uom = uom.uom

            filter_ubuntu_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
            if filter_ubuntu_uom:
                if (udf_calmethod!= filter_ubuntu_uom.udfcalmethod) or (udf_calrate!=filter_ubuntu_uom.udfcalrate):
                    update = ItemUOM.objects.get(itemcode=item_code,uom=uom)
                    update.udfcalmethod = udf_calmethod
                    update.udfcalrate = udf_calrate
                    update.save()
    
    filter_book1_uom = AcItemUOM.objects.using('windows_server_book2').filter(udfcalrate__gt=0)
    if filter_book1_uom:
        for uom in filter_book1_uom:
            udf_calmethod = uom.udfcalmethod
            udf_calrate = uom.udfcalrate
            item_code = uom.itemcode
            uom = uom.uom

            filter_ubuntu_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
            if filter_ubuntu_uom:
                if (udf_calmethod!= filter_ubuntu_uom.udfcalmethod) or (udf_calrate!=filter_ubuntu_uom.udfcalrate):
                    update = ItemUOM.objects.get(itemcode=item_code,uom=uom)
                    update.udfcalmethod = udf_calmethod
                    update.udfcalrate = udf_calrate
                    update.save()
    
    # return
    ### update udfpallet
    filter_ubuntu_uom_pallet = ItemUOM.objects.filter(udfispallet__gt=0)
    
    if filter_ubuntu_uom_pallet:
        for uom_pallet in filter_ubuntu_uom_pallet:
            udf_ispallet = uom_pallet.udfispallet
            item_code = uom_pallet.itemcode.itemcode
            uom = uom_pallet.uom
            
            filter_book1_uom = AcItemUOM.objects.using('windows_server').filter(itemcode=item_code,uom=uom).first()
            filter_book2_uom = AcItemUOM.objects.using('windows_server_book2').filter(itemcode=item_code,uom=uom).first()

            if filter_book1_uom:
                book1_udfpallet = int(filter_book1_uom.udfispallet)
                if udf_ispallet != book1_udfpallet:
                    uom_pallet.udfispallet = book1_udfpallet
                    print('book 1')
                    uom_pallet.save()
            
            if filter_book2_uom:
                book2_udfpallet = int(filter_book2_uom.udfispallet)
                if (udf_ispallet != book2_udfpallet):
                    uom_pallet.udfispallet = book2_udfpallet
                    print('book 2')
                    print(item_code, udf_ispallet, book2_udfpallet)
                    uom_pallet.save()
    # return
                    
    filter_book1_uom_pallet = AcItemUOM.objects.using('windows_server').filter(udfispallet__gt=0)
    # print(filter_book1_uom_pallet.itemcode)
    # return
    if filter_book1_uom_pallet:
        for uom_pallet in filter_book1_uom_pallet:
            udf_ispallet = int(uom_pallet.udfispallet)
            item_code = uom_pallet.itemcode
            uom = uom_pallet.uom

            filter_ubuntu_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
            if filter_ubuntu_uom:
                ubuntu_udfpallet = filter_ubuntu_uom.udfispallet
                if (udf_ispallet != ubuntu_udfpallet):
                    filter_ubuntu_uom.udfispallet = udf_ispallet
                    print('book 3')
                    print(item_code,udf_ispallet, ubuntu_udfpallet)
                    filter_ubuntu_uom.save()
    
    filter_book2_uom_pallet = AcItemUOM.objects.using('windows_server_book2').filter(udfispallet__gt=0)
    if filter_book2_uom_pallet:
        for uom_pallet in filter_book2_uom_pallet:
            udf_ispallet = int(uom_pallet.udfispallet)
            item_code = uom_pallet.itemcode
            uom = uom_pallet.uom

            filter_ubuntu_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
            if filter_ubuntu_uom:
                ubuntu_udfpallet = filter_ubuntu_uom.udfispallet
                if (udf_ispallet != ubuntu_udfpallet):
                    filter_ubuntu_uom.udfispallet = udf_ispallet
                    print('4')
                    filter_ubuntu_uom.save()

def import_salesagent_from_autocount():
    new_agents_to_create = []
    autocount_server_salesagent = AcSalesAgent.objects.using('windows_server').all()
    # autocount_server_salesagent_book3 = AcSalesAgent.objects.using('windows_server_book3').all()
    
    combined_sales_agent = list(chain(autocount_server_salesagent))

    # Fetch all existing salesagent values in one query
    existing_salesagents = set(SalesAgent.objects.values_list('salesagent', flat=True))

    for salesagent in combined_sales_agent:
        sales_agent = salesagent.salesagent

        if sales_agent not in existing_salesagents and not any(existing_salesagent.salesagent == sales_agent for existing_salesagent in new_agents_to_create):
            print(sales_agent)
            new_agent = SalesAgent(autokey=panda.panda_uuid(),guid=panda.panda_uuid(),salesagent=sales_agent, lastupdate=0,isactive=1)
            new_agents_to_create.append(new_agent)

    with transaction.atomic():
        # Bulk create SalesAgent
        if new_agents_to_create:
            SalesAgent.objects.bulk_create(new_agents_to_create)

def import_terms_from_autocount(tempcompanyautokey):
    autocount_server_terms = AcTerms.objects.using('windows_server').all()
    # autocount_server_terms_book3 = AcTerms.objects.using('windows_server_book3').all()

    combined_terms = list(chain(autocount_server_terms))

    existing_displayterms = set(Terms.objects.values_list('displayterm', flat=True))
    new_terms = []

    for term in combined_terms:
        display_term = term.displayterm
        terms = term.terms

        if display_term not in existing_displayterms and not any(term.displayterm == display_term for term in new_terms):
            new_term = Terms(autokey=panda.panda_uuid(),displayterm=display_term, terms=terms, lastupdate= 0, companyautokey=tempcompanyautokey)
            new_terms.append(new_term)
    
    with transaction.atomic():
        # Bulk create all new terms in a single query
        if new_terms:
            Terms.objects.bulk_create(new_terms)

def import_debtors_from_autocount(tempcompanyautokey):
    autocount_server_debtors = AcDebtor.objects.using('windows_server').values_list(
    'accno', 'companyname', 'currencycode', 'discountpercent', 'allowexceedcreditlimit', 
    'isactive', 'inclusivetax', 'displayterm', 'udfispallet'
)
    
    combined_debtors = list(chain(autocount_server_debtors))

    existing_debtors = set(Debtor.objects.values_list('accno', flat=True))

    terms_dict = {term.displayterm: term for term in Terms.objects.all()}

    new_debtors = []

    for acc_no, company_name, currency_code, discount_percent, allow_exceed_credit_limit, is_active, inclusive_tax, display_term, udf_ispallet in combined_debtors:
        if acc_no not in existing_debtors and not any(debtor.accno == acc_no for debtor in new_debtors):
            # Get the Terms object from the dictionary
            filter_display_term = terms_dict.get(display_term)

            new_debtor = Debtor(
                autokey=panda.panda_uuid(),
                guid=panda.panda_uuid(),
                accno=acc_no,
                companyname=company_name,
                displayterm=filter_display_term,
                currencycode=currency_code,
                allowexceedcreditlimit=allow_exceed_credit_limit,
                discountpercent=discount_percent,
                lastmodified=datetime.now(),
                lastmodifieduserid='NA',
                hasbonuspoint='F',
                isgroupcompany='F',
                isactive=is_active,
                lastupdate=0,
                inclusivetax=inclusive_tax,
                roundingmethod=-1,
                companyautokey=tempcompanyautokey,
                selfbilledapprovalno=0,
                udfispallet= udf_ispallet
            )
            new_debtors.append(new_debtor)

    with transaction.atomic():
        if new_debtors:
            Debtor.objects.bulk_create(new_debtors)

    filter_windows_debtor_udf = Debtor.objects.filter(udfispallet__gt=0)
    for debtor in filter_windows_debtor_udf:
        debtor_code = debtor.accno
        last_modified = debtor.lastmodified
        udf_ispallet = debtor.udfispallet

        filter_book1_debtor = AcDebtor.objects.using('windows_server').filter(accno=debtor_code).first()
        book1_last_modified = filter_book1_debtor.lastmodified
        book1_udf_ispallet = filter_book1_debtor.udfispallet

        if (book1_last_modified > last_modified) & (udf_ispallet != book1_udf_ispallet):
            debtor.lastmodified = book1_last_modified
            debtor.udfispallet = book1_udf_ispallet
            debtor.save()
    

        filter_book2_debtor = AcDebtor.objects.using('windows_server_book2').filter(accno=debtor_code).first()
        book2_last_modified = filter_book2_debtor.lastmodified
        book2_udf_ispallet = filter_book2_debtor.udfispallet

        if (book2_last_modified > last_modified) & (udf_ispallet != book2_udf_ispallet):
            debtor.lastmodified = book2_last_modified
            debtor.udfispallet = book2_udf_ispallet
            debtor.save()

    filter_book1_debtor = AcDebtor.objects.using('windows_server').filter(udfispallet__gt=0)
    for book1 in filter_book1_debtor:
        book1_debtor_code = book1.accno
        book1_last_modified = book1.lastmodified
        book1_udf_ispallet = book1.udfispallet

        filter_ubuntu_debtor = Debtor.objects.filter(accno=book1_debtor_code).first()
        last_modified = filter_ubuntu_debtor.lastmodified
        udf_ispallet = filter_ubuntu_debtor.udfispallet
        if (book1_last_modified > last_modified) & (udf_ispallet != book1_udf_ispallet):
            filter_ubuntu_debtor.lastmodified = book1_last_modified
            filter_ubuntu_debtor.udfispallet = book1_udf_ispallet
            filter_ubuntu_debtor.save()

    filter_book2_debtor = AcDebtor.objects.using('windows_server_book2').filter(udfispallet__gt=0)
    for book2 in filter_book2_debtor:
        book2_debtor_code = book2.accno
        book2_last_modified = book2.lastmodified
        book2_udf_ispallet = book2.udfispallet

        filter_ubuntu_debtor = Debtor.objects.filter(accno=book2_debtor_code).first()
        last_modified = filter_ubuntu_debtor.lastmodified
        udf_ispallet = filter_ubuntu_debtor.udfispallet
        if (book2_last_modified > last_modified) & (udf_ispallet != book2_udf_ispallet):
            filter_ubuntu_debtor.lastmodified = book2_last_modified
            filter_ubuntu_debtor.udfispallet = book2_udf_ispallet
            filter_ubuntu_debtor.save()

def add_lorry_crew_transaction(lorry_guid,doc_no,tempcompanyautokey):

    import_item_from_autocount(tempcompanyautokey)

    import_itemuom_from_autocount(tempcompanyautokey)
    
    import_salesagent_from_autocount()

    import_terms_from_autocount(tempcompanyautokey)

    import_debtors_from_autocount(tempcompanyautokey)

    

    
    

    # return
    all_docno = []
    print(lorry_guid, doc_no)
    lorry_guid = Lorry.objects.get(lorryguid=lorry_guid)

    error = {'request': 'POST', 'response': '', 'status': ''}

    is_iv_exists_in_ubuntu = IV.objects.filter(docno=doc_no).exists()
    
    exists_in_ubuntu = False
    exists_in_windows_book1 = False
    exists_in_windows_book2 = False
    exists_in_windows_book3 = False

    if not is_iv_exists_in_ubuntu:
        is_iv_exists_windows_server = AcIV.objects.using('windows_server').filter(docno=doc_no).exists()
        if not is_iv_exists_windows_server:
            is_iv_exists_windows_server_book3 = AcIV.objects.using('windows_server_book3').filter(docno=doc_no).exists()
            if not is_iv_exists_windows_server_book3:
                is_iv_exists_windows_server_book2 = AcIV.objects.using('windows_server_book2').filter(docno=doc_no).exists()
                if not is_iv_exists_windows_server_book2:
                    error['response'] = 'Invoice Not Found In Book 1, 2, and 3'
                    error['status'] = status.HTTP_404_NOT_FOUND
                    return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                else:
                    exists_in_windows_book2 = True
            else:
                exists_in_windows_book3 = True
        else:
            exists_in_windows_book1 = True
    else:
        exists_in_ubuntu = True

    # ubuntu
    if exists_in_ubuntu:
        print('im ubuntu')
        filter_iv = IV.objects.filter(docno=doc_no).first()
        invoice_date = filter_iv.docdate
        invoice_no = filter_iv.docno
        debtor_code = filter_iv.debtorcode.accno
        debtor_name = filter_iv.debtorname
        transaction_dtl_list = []
        rebate_ivdtl_list = []

        is_transaction_exists = Transaction.objects.filter(docno=invoice_no).exists()
        if not is_transaction_exists:
            new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
            new_transaction.save()
            get_transaction_guid = new_transaction
            iv = IV.objects.only("autokey").get(docno=invoice_no)
            filter_ivdtl = IVDTL.objects.filter(headerautokey=iv.autokey)

            rebate_children = None
            filter_windows_rebate_dockey = None
            used_db = None

            if AcIV.objects.using('windows_server').filter(docno=doc_no).exists():
                used_db = 'windows_server'
                filter_windows_rebate_dockey = AcIV.objects.using(used_db).filter(docno=doc_no).first().dockey
                rebate_children = AcIVDTL.objects.using(used_db).filter(
                    dockey=filter_windows_rebate_dockey, description__icontains='rebate'
                )
            elif AcIV.objects.using('windows_server_book2').filter(docno=doc_no).exists():
                used_db = 'windows_server_book2'
                filter_windows_rebate_dockey = AcIV.objects.using(used_db).filter(docno=doc_no).first().dockey
                rebate_children = AcIVDTL.objects.using(used_db).filter(
                    dockey=filter_windows_rebate_dockey, description__icontains='rebate'
                )
            elif AcIV.objects.using('windows_server_book3').filter(docno=doc_no).exists():
                used_db = 'windows_server_book3'
                filter_windows_rebate_dockey = AcIV.objects.using(used_db).filter(docno=doc_no).first().dockey
                rebate_children = AcIVDTL.objects.using(used_db).filter(
                    dockey=filter_windows_rebate_dockey, description__icontains='discount'
                )

            if rebate_children:
                iv_headerautokey=IV.objects.get(docno=doc_no)
                autocount_ivdtl = AcIVDTL.objects.using(used_db).filter(dockey=filter_windows_rebate_dockey)
                filter_ivdtl = IVDTL.objects.filter(headerautokey=iv_headerautokey.autokey)

                if autocount_ivdtl.count() != filter_ivdtl.count():
                    filter_ivdtl.delete()
                    for seq, ivdtl in enumerate(autocount_ivdtl, start=1):
                        if ivdtl.itemcode:
                            uom = ivdtl.uom
                            # item_autokey = ivdtl.itemcode
                            # print(item_autokey)
                            item_code_instance = Item.objects.filter(itemcode=ivdtl.itemcode).first()
                            item_class_value = item_code_instance.itemclass
                            item_code = item_code_instance.itemcode
                            description = ivdtl.description
                            quantity = ivdtl.qty
                            sub_total = ivdtl.subtotal
                            rate = ivdtl.rate
                            smallestqty = ivdtl.smallestqty
                            transferedqty = ivdtl.transferedqty
                            smallestunitprice = ivdtl.smallestunitprice
                            unitprice = ivdtl.unitprice
                            discount= ivdtl.discount
                            discountamt = ivdtl.discountamt
                            location = Location.objects.filter(location='REBATE').first()

                            # print(item_class_value,item_code)
                            if not item_class_value:
                                # DELETE THE ADDED TRANSACTION HEADER
                                print('t-1')
                                new_transaction.delete()
                                error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                                error['status'] = status.HTTP_404_NOT_FOUND
                                return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                            # return

                            item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                            comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                            new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=sub_total,uom=uom, commtype=comm_type)
                            rebate_ivdtl = IVDTL(autokey=panda_uuid(),guid=panda_uuid(),seq=seq,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallestqty,transferedqty=transferedqty,smallestunitprice=smallestunitprice,unitprice=unitprice,discount=discount,discountamt=discountamt,subtotal=sub_total,localsubtotal=sub_total,subtotalextax=sub_total,taxableamt=sub_total,localsubtotalextax=sub_total,localtaxableamt=sub_total,taxcurrencytaxableamt=sub_total,headerautokey=iv_headerautokey,itemcode=item_code_instance,location=location)
                            transaction_dtl_list.append(new_transaction_dtl)
                            rebate_ivdtl_list.append(rebate_ivdtl)
                else:
                    for ivdtl in filter_ivdtl:
                        if ivdtl.itemcode:
                            uom = ivdtl.uom
                            item_autokey = ivdtl.itemcode
                            item_code_instance = Item.objects.filter(autokey=item_autokey).first()
                            item_class_value = item_code_instance.itemclass
                            item_code = item_code_instance.itemcode
                            description = ivdtl.description
                            quantity = ivdtl.qty
                            sub_total = ivdtl.subtotal

                            if not item_class_value:
                                # DELETE THE ADDED TRANSACTION HEADER
                                print('t-2')
                                new_transaction.delete()
                                error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                                error['status'] = status.HTTP_404_NOT_FOUND
                                return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)

                            item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                            comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                            new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=sub_total,uom=uom, commtype=comm_type)
                            transaction_dtl_list.append(new_transaction_dtl)
                    
            else:    
                for ivdtl in filter_ivdtl:
                    if ivdtl.itemcode:
                        item_code = ivdtl.itemcode
                        description = ivdtl.description
                        quantity = ivdtl.qty
                        sub_total = ivdtl.subtotal
                        uom = ivdtl.uom
                        filter_item = Item.objects.filter(autokey=item_code).first()
                        item_class_value = filter_item.itemclass
                        item_code = filter_item.itemcode

                        if not item_class_value:
                            # DELETE THE ADDED TRANSACTION HEADER
                            print('t-3')
                            new_transaction.delete()
                            error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                            error['status'] = status.HTTP_404_NOT_FOUND
                            return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                        
                        item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                        
                        comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                        new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=sub_total, uom=uom, commtype=comm_type)
                        transaction_dtl_list.append(new_transaction_dtl)
                        # new_transaction_dtl.save()

            if rebate_ivdtl_list:
                IVDTL.objects.bulk_create(rebate_ivdtl_list)
            TransactionDtl.objects.bulk_create(transaction_dtl_list)
                    
            
            # Return all docno
            filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno').values_list('docno', flat=True)
            all_docno = list(filter_docno)
            return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)
        else:
            is_lorry_invoice_exists = Transaction.objects.filter(docno=invoice_no,lorryguid=lorry_guid).exists()
            if not is_lorry_invoice_exists:
                new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
                new_transaction.save()
                get_transaction_guid = new_transaction
                filter_ivdtl = IVDTL.objects.filter(headerautokey=IV.objects.get(docno=invoice_no).autokey)

                rebate_children = None
                filter_windows_rebate_dockey = None
                used_db = None
                
                if AcIV.objects.using('windows_server').filter(docno=doc_no).exists():
                    used_db = 'windows_server'
                    filter_windows_rebate_dockey = AcIV.objects.using(used_db).filter(docno=doc_no).first().dockey
                    rebate_children = AcIVDTL.objects.using(used_db).filter(
                        dockey=filter_windows_rebate_dockey, description__icontains='rebate', subtotal__lt=0
                    )
                elif AcIV.objects.using('windows_server_book2').filter(docno=doc_no).exists():
                    used_db = 'windows_server_book2'
                    filter_windows_rebate_dockey = AcIV.objects.using(used_db).filter(docno=doc_no).first().dockey
                    rebate_children = AcIVDTL.objects.using(used_db).filter(
                        dockey=filter_windows_rebate_dockey, description__icontains='rebate', subtotal__lt=0
                )
                    
                if rebate_children:
                    iv_headerautokey=IV.objects.get(docno=doc_no)
                    autocount_ivdtl = AcIVDTL.objects.using(used_db).filter(dockey=filter_windows_rebate_dockey)
                    filter_ivdtl = IVDTL.objects.filter(headerautokey=iv_headerautokey.autokey)
                    
                    if autocount_ivdtl.count() != filter_ivdtl.count():
                        filter_ivdtl.delete()
                        for seq, ivdtl in enumerate(autocount_ivdtl, start=1):
                            if ivdtl.itemcode:
                                uom = ivdtl.uom
                                # item_autokey = ivdtl.itemcode
                                # print(item_autokey)
                                item_code_instance = Item.objects.filter(itemcode=ivdtl.itemcode).first()
                                item_class_value = item_code_instance.itemclass
                                item_code = item_code_instance.itemcode
                                description = ivdtl.description
                                quantity = ivdtl.qty
                                sub_total = ivdtl.subtotal
                                rate = ivdtl.rate
                                smallestqty = ivdtl.smallestqty
                                transferedqty = ivdtl.transferedqty
                                smallestunitprice = ivdtl.smallestunitprice
                                unitprice = ivdtl.unitprice
                                discount= ivdtl.discount
                                discountamt = ivdtl.discountamt
                                location = Location.objects.filter(location='REBATE').first()

                                # print(item_class_value,item_code)
                                if not item_class_value:
                                    # DELETE THE ADDED TRANSACTION HEADER
                                    print('t-4')
                                    new_transaction.delete()
                                    error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                                    error['status'] = status.HTTP_404_NOT_FOUND
                                    return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                                # return

                                item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                                comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                                new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=sub_total,uom=uom, commtype=comm_type)
                                rebate_ivdtl = IVDTL(autokey=panda_uuid(),guid=panda_uuid(),seq=seq,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallestqty,transferedqty=transferedqty,smallestunitprice=smallestunitprice,unitprice=unitprice,discount=discount,discountamt=discountamt,subtotal=sub_total,localsubtotal=sub_total,subtotalextax=sub_total,taxableamt=sub_total,localsubtotalextax=sub_total,localtaxableamt=sub_total,taxcurrencytaxableamt=sub_total,headerautokey=iv_headerautokey,itemcode=item_code_instance,location=location)
                                transaction_dtl_list.append(new_transaction_dtl)
                                rebate_ivdtl_list.append(rebate_ivdtl)
                    else:
                        for ivdtl in filter_ivdtl:
                            if ivdtl.itemcode:
                                uom = ivdtl.uom
                                item_autokey = ivdtl.itemcode
                                item_code_instance = Item.objects.filter(autokey=item_autokey).first()
                                item_class_value = item_code_instance.itemclass
                                item_code = item_code_instance.itemcode
                                description = ivdtl.description
                                quantity = ivdtl.qty
                                sub_total = ivdtl.subtotal

                                if not item_class_value:
                                    # DELETE THE ADDED TRANSACTION HEADER
                                    print('t-5')
                                    new_transaction.delete()
                                    error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                                    error['status'] = status.HTTP_404_NOT_FOUND
                                    return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)

                                item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                                comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                                new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=sub_total,uom=uom, commtype=comm_type)
                                transaction_dtl_list.append(new_transaction_dtl)
                else:
                    for ivdtl in filter_ivdtl:
                        if ivdtl.itemcode:
                            uom = ivdtl.uom
                            item_autokey = ivdtl.itemcode
                            item_code_instance = Item.objects.filter(autokey=item_autokey).first()
                            item_class_value = item_code_instance.itemclass
                            item_code = item_code_instance.itemcode
                            description = ivdtl.description
                            quantity = ivdtl.qty
                            sub_total = ivdtl.subtotal

                            if item_class_value:
                                previous_itemclass = item_class_value

                            if not item_class_value and 'Discount' in description and sub_total <0:
                                item_class_value = previous_itemclass

                            if not item_class_value:
                                # DELETE THE ADDED TRANSACTION HEADER
                                print('t-6')
                                new_transaction.delete()
                                error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                                error['status'] = status.HTTP_404_NOT_FOUND
                                return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)

                            item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                            comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                            new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=sub_total,uom=uom, commtype=comm_type)
                            transaction_dtl_list.append(new_transaction_dtl)
                
                if rebate_ivdtl_list:
                    IVDTL.objects.bulk_create(rebate_ivdtl_list)
                TransactionDtl.objects.bulk_create(transaction_dtl_list)
                # Return all docno
                filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno')
                for docno in filter_docno:
                    all_docno.append(docno.docno)
                return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)
            else:
                error['response'] = 'Invoice Exists For This Lorry'
                error['status'] = status.HTTP_409_CONFLICT
                return JsonResponse(error, safe=False, status=status.HTTP_409_CONFLICT)

    # book 1
    if exists_in_windows_book1:
            print('im book1')
            print('1')
            is_iv_exists_windows_server = AcIV.objects.using('windows_server').filter(docno=doc_no).first()
            sales_agent = is_iv_exists_windows_server.salesagent
            
            display_term = Terms.objects.filter(displayterm=is_iv_exists_windows_server.displayterm).first()
            doc_key = is_iv_exists_windows_server.dockey
            invoice_date = is_iv_exists_windows_server.docdate
            invoice_no = is_iv_exists_windows_server.docno
            debtor_code_instsance = Debtor.objects.get(accno=is_iv_exists_windows_server.debtorcode)
            debtor_code = is_iv_exists_windows_server.debtorcode
            debtor_name = is_iv_exists_windows_server.debtorname
            description = is_iv_exists_windows_server.description
            total_invoice_amount = is_iv_exists_windows_server.total
            currency_code = is_iv_exists_windows_server.currencycode
            currency_rate = is_iv_exists_windows_server.currencyrate
            post_to_stock = is_iv_exists_windows_server.posttostock
            post_to_gl = is_iv_exists_windows_server.posttogl
            transferable = is_iv_exists_windows_server.transferable
            print_count = is_iv_exists_windows_server.printcount
            last_modified = is_iv_exists_windows_server.lastmodified
            lastmodifieduserid = is_iv_exists_windows_server.lastmodifieduserid
            cancelled = is_iv_exists_windows_server.cancelled
            created_time_stamp = is_iv_exists_windows_server.createdtimestamp
            can_sync = is_iv_exists_windows_server.cansync
            last_update = is_iv_exists_windows_server.lastupdate
            reallocate_purchase_by_project = is_iv_exists_windows_server.reallocatepurchasebyproject
            to_tax_currency_rate = is_iv_exists_windows_server.totaxcurrencyrate
            rounding_method = is_iv_exists_windows_server.roundingmethod
            location = Location.objects.get(location='NA') 
            
            ivdtl_windows_server = AcIVDTL.objects.using('windows_server').filter(dockey=doc_key)

            item_code = AcIVDTL.objects.using('windows_server').filter(dockey=doc_key).exclude(
                Q(itemcode__isnull=True) | Q(itemcode='')
            ).first().itemcode
            
            get_item_group_from_ivdtl = AcItem.objects.using('windows_server').filter(itemcode=item_code).first().itemgroup

            if not sales_agent:
                sales_agent = SalesAgent.objects.get(salesagent='NA')
            else:
                sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            
            if get_item_group_from_ivdtl:
                filter_branch = Branch.objects.filter(address=get_item_group_from_ivdtl).first()
                if not filter_branch:
                    new_branch = Branch(address=get_item_group_from_ivdtl, companyautokey=tempcompanyautokey)
                    new_branch.save()

                    filter_branch = Branch.objects.get(address=get_item_group_from_ivdtl)
            else:
                filter_branch = Branch.objects.get(address='NA')
            # need to add lorry driver due to can't migrate
            new_iv = IV(udfbook='1',lorrydriver='NA',salesagent=sales_agent,displayterm=display_term,branchautokey=filter_branch,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code_instsance,debtorname=debtor_name,description=description,total=total_invoice_amount,nettotal=total_invoice_amount,localnettotal=total_invoice_amount,analysisnettotal=total_invoice_amount,finaltotal=total_invoice_amount,localtaxableamt=total_invoice_amount,taxcurrencytaxableamt=total_invoice_amount,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=last_modified,lastmodifieduserid=lastmodifieduserid,createdtimestamp=created_time_stamp,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
            new_transaction.save()

            get_iv_guid = IV.objects.get(docno=invoice_no)
            get_transaction_guid = Transaction.objects.filter(docno=invoice_no).first()
            
            ivdtl_list = []
            transaction_dtl_list = []
            
            for ivdtl in ivdtl_windows_server:
                if ivdtl.itemcode or ivdtl.subtotal or ivdtl.qty:
                    if ivdtl.itemcode:
                        if not ivdtl.focqty:
                            seq = ivdtl.seq
                            main_item = ivdtl.mainitem
                            item_code = ivdtl.itemcode
                            uom = ivdtl.uom
                            rate = ivdtl.rate
                            unit_price = ivdtl.unitprice
                            filter_itemcode = Item.objects.filter(itemcode=item_code).first()
                            if not filter_itemcode:
                                filter_windows_item = AcItem.objects.using('windows_server').filter(itemcode=item_code).first()
                                item_brand = 'NA'
                                description = filter_windows_item.description
                                mainsupplier = 'book1'
                                last_modified = filter_windows_item.lastmodified
                                item_class = filter_windows_item.itemclass
                                

                                save_new_item = Item(itembrand=item_brand,itemcode=item_code,description=description,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=last_modified,lastupdate=0,itemclass=item_class)
                                save_new_item.save()

                                item_code_instance = Item.objects.get(itemcode = item_code)
                                
                                filter_windows_uom = AcItemUOM.objects.using('windows_server').filter(itemcode=item_code).first()
                                udf_calmethod = filter_windows_uom.udfcalmethod
                                udf_calrate = filter_windows_uom.udfcalrate
                                # udf_pallet = filter_windows_uom.udfpallet
                                # , udfpallet=udf_pallet # add this
                                save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=item_code_instance,uom=uom,rate=rate,price=unit_price,lastupdate=0,udfcalmethod=udf_calmethod,udfcalrate=udf_calrate)
                                save_uom.save()
                            else:
                                filter_uom = ItemUOM.objects.filter(itemcode=item_code,uom=uom).first()
                                item_code_instance = Item.objects.get(itemcode = item_code)
                                if not filter_uom:
                                    filter_windows_uom = AcItemUOM.objects.using('windows_server').filter(itemcode=item_code).first()
                                    udf_calmethod = filter_windows_uom.udfcalmethod
                                    udf_calrate = filter_windows_uom.udfcalrate
                                    # udf_pallet = filter_windows_uom.udfpallet
                                    # , udfpallet=udf_pallet # add this
                                    save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=item_code_instance,uom=uom,rate=rate,price=unit_price,lastupdate=0,udfcalmethod=udf_calmethod,udfcalrate=udf_calrate)
                                    save_uom.save()
                            

                            quantity = ivdtl.qty
                            if not quantity:
                                quantity = ivdtl.focqty
                            smallest_qty = ivdtl.smallestqty
                            smallest_unit_price =ivdtl.smallestunitprice
                            net_amount = ivdtl.subtotal
                            description = ivdtl.description
                            item_class_value = item_code_instance.itemclass
                            item_code = item_code_instance.itemcode
                            # print(item_code,uom,quantity,rate,smallest_qty,unit_price,discount_amount,net_amount,description,item_class_value)
                            if not item_class_value:
                                # DELETE THE ADDED TRANSACTION HEADER
                                print('1')
                                new_iv.delete()
                                new_transaction.delete()
                                error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                                error['status'] = status.HTTP_404_NOT_FOUND
                                return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                            
                            item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                            comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                            new_ivdtl = IVDTL(autokey=panda_uuid(),guid=panda_uuid(),seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
                            ivdtl_list.append(new_ivdtl)
                            # new_ivdtl.save()
                            
                            new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=net_amount, uom=uom, commtype=comm_type)
                            transaction_dtl_list.append(new_transaction_dtl)
                            # new_transaction_dtl.save()
                    else:
                        item_code_instance = Item.objects.get(itemcode = 'BOOK1-DISCOUNT')
                        seq = ivdtl.seq
                        main_item = ivdtl.mainitem
                        item_code = "BOOK1-DISCOUNT"
                        uom = None
                        rate = 1
                        unit_price = None

                        quantity = 1
                        smallest_qty = ivdtl.smallestqty
                        smallest_unit_price = None
                        net_amount = ivdtl.subtotal
                        description = ivdtl.description
                        item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass='SUNDRY($)')
                        comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                        new_ivdtl = IVDTL(autokey=panda_uuid(),guid=panda_uuid(),seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
                        ivdtl_list.append(new_ivdtl)

                        new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=net_amount, uom=uom, commtype=comm_type)
                        transaction_dtl_list.append(new_transaction_dtl)

            with transaction.atomic():
                IVDTL.objects.bulk_create(ivdtl_list)
                TransactionDtl.objects.bulk_create(transaction_dtl_list)

            # Return all docno
            filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno').values_list('docno', flat=True)
            all_docno = list(filter_docno)
            return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)

    # book 2
    if exists_in_windows_book2:
            print('im book 2')
            print('2')
            is_iv_exists_windows_server_book2 = AcIV.objects.using('windows_server_book2').filter(docno=doc_no).first()
            sales_agent = is_iv_exists_windows_server_book2.salesagent
            
            display_term = Terms.objects.filter(displayterm=is_iv_exists_windows_server_book2.displayterm).first()
            doc_key = is_iv_exists_windows_server_book2.dockey
            invoice_date = is_iv_exists_windows_server_book2.docdate
            invoice_no = is_iv_exists_windows_server_book2.docno
            debtor_code_instsance = Debtor.objects.get(accno=is_iv_exists_windows_server_book2.debtorcode)
            debtor_code = is_iv_exists_windows_server_book2.debtorcode
            debtor_name = is_iv_exists_windows_server_book2.debtorname
            description = is_iv_exists_windows_server_book2.description
            total_invoice_amount = is_iv_exists_windows_server_book2.total
            currency_code = is_iv_exists_windows_server_book2.currencycode
            currency_rate = is_iv_exists_windows_server_book2.currencyrate
            post_to_stock = is_iv_exists_windows_server_book2.posttostock
            post_to_gl = is_iv_exists_windows_server_book2.posttogl
            transferable = is_iv_exists_windows_server_book2.transferable
            print_count = is_iv_exists_windows_server_book2.printcount
            last_modified = is_iv_exists_windows_server_book2.lastmodified
            lastmodifieduserid = is_iv_exists_windows_server_book2.lastmodifieduserid
            cancelled = is_iv_exists_windows_server_book2.cancelled
            created_time_stamp = is_iv_exists_windows_server_book2.createdtimestamp
            can_sync = is_iv_exists_windows_server_book2.cansync
            last_update = is_iv_exists_windows_server_book2.lastupdate
            reallocate_purchase_by_project = is_iv_exists_windows_server_book2.reallocatepurchasebyproject
            to_tax_currency_rate = is_iv_exists_windows_server_book2.totaxcurrencyrate
            rounding_method = is_iv_exists_windows_server_book2.roundingmethod
            location = Location.objects.get(location='NA') 

            ivdtl_windows_server = AcIVDTL.objects.using('windows_server_book2').filter(dockey=doc_key)
            item_code = AcIVDTL.objects.using('windows_server_book2').filter(dockey=doc_key).first().itemcode
            get_item_group_from_ivdtl = AcItem.objects.using('windows_server_book2').filter(itemcode=item_code).first().itemgroup

            if not sales_agent:
                sales_agent = SalesAgent.objects.get(salesagent='NA')
            else:
                sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            
            if get_item_group_from_ivdtl:
                filter_branch = Branch.objects.filter(address=get_item_group_from_ivdtl).first()
                if not filter_branch:
                    new_branch = Branch(address=get_item_group_from_ivdtl, companyautokey=tempcompanyautokey)
                    new_branch.save()

                    filter_branch = Branch.objects.get(address=get_item_group_from_ivdtl)
            else:
                filter_branch = Branch.objects.get(address='NA')
            # need to add lorry driver due to can't migrate
            new_iv = IV(udfbook='1',lorrydriver='NA',salesagent=sales_agent,displayterm=display_term,branchautokey=filter_branch,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code_instsance,debtorname=debtor_name,description=description,total=total_invoice_amount,nettotal=total_invoice_amount,localnettotal=total_invoice_amount,analysisnettotal=total_invoice_amount,finaltotal=total_invoice_amount,localtaxableamt=total_invoice_amount,taxcurrencytaxableamt=total_invoice_amount,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=last_modified,lastmodifieduserid=lastmodifieduserid,createdtimestamp=created_time_stamp,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
            new_transaction.save()

            get_iv_guid = IV.objects.get(docno=invoice_no)
            get_transaction_guid = Transaction.objects.filter(docno=invoice_no).first()
            
            ivdtl_list = []
            transaction_dtl_list = []
            
            for ivdtl in ivdtl_windows_server:
                if ivdtl.itemcode:

                    seq = ivdtl.seq
                    main_item = ivdtl.mainitem
                    item_code = ivdtl.itemcode
                    uom = ivdtl.uom
                    rate = ivdtl.rate
                    unit_price = ivdtl.unitprice
                    filter_itemcode = Item.objects.filter(itemcode=item_code).first()
                    if not filter_itemcode:
                        filter_windows_item = AcItem.objects.using('windows_server_book2').filter(itemcode=item_code).first()
                        item_brand = 'NA'
                        description = filter_windows_item.description
                        mainsupplier = 'book1'
                        last_modified = filter_windows_item.lastmodified
                        item_class = filter_windows_item.itemclass
                        

                        save_new_item = Item(itembrand=item_brand,itemcode=item_code,description=description,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=last_modified,lastupdate=0,itemclass=item_class)
                        save_new_item.save()

                        item_code_instance = Item.objects.get(itemcode = item_code)
                        
                        filter_windows_uom = AcItemUOM.objects.using('windows_server_book2').filter(itemcode=item_code).first()
                        udf_calmethod = filter_windows_uom.udfcalmethod
                        udf_calrate = filter_windows_uom.udfcalrate
                        # udf_pallet = filter_windows_uom.udfpallet
                        # , udfpallet=udf_pallet # add this
                        save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=item_code_instance,uom=uom,rate=rate,price=unit_price,lastupdate=0,udfcalmethod=udf_calmethod,udfcalrate=udf_calrate)
                        save_uom.save()
                    else:
                        filter_uom = ItemUOM.objects.filter(itemcode=item_code,uom=uom).first()
                        item_code_instance = Item.objects.get(itemcode = item_code)
                        if not filter_uom:
                            filter_windows_uom = AcItemUOM.objects.using('windows_server_book2').filter(itemcode=item_code).first()
                            udf_calmethod = filter_windows_uom.udfcalmethod
                            udf_calrate = filter_windows_uom.udfcalrate
                            # udf_pallet = filter_windows_uom.udfpallet
                            # , udfpallet=udf_pallet # add this
                            save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=item_code_instance,uom=uom,rate=rate,price=unit_price,lastupdate=0,udfcalmethod=udf_calmethod,udfcalrate=udf_calrate)
                            save_uom.save()
                    

                    quantity = ivdtl.qty
                    if not quantity:
                        quantity = ivdtl.focqty
                    smallest_qty = ivdtl.smallestqty
                    smallest_unit_price =ivdtl.smallestunitprice
                    net_amount = ivdtl.subtotal
                    description = ivdtl.description

                    item_class_value = item_code_instance.itemclass
                    item_code = item_code_instance.itemcode
                    # print(item_code,uom,quantity,rate,smallest_qty,unit_price,discount_amount,net_amount,description,item_class_value)
                    if not item_class_value:
                        # DELETE THE ADDED TRANSACTION HEADER
                        print('1')
                        new_iv.delete()
                        new_transaction.delete()
                        error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                        error['status'] = status.HTTP_404_NOT_FOUND
                        return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                    
                    item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                    comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                    new_ivdtl = IVDTL(autokey=panda_uuid(),guid=panda_uuid(),seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
                    ivdtl_list.append(new_ivdtl)
                    # new_ivdtl.save()
                    
                    new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=net_amount, uom=uom, commtype=comm_type)
                    transaction_dtl_list.append(new_transaction_dtl)
                    # new_transaction_dtl.save()

            with transaction.atomic():
                IVDTL.objects.bulk_create(ivdtl_list)
                TransactionDtl.objects.bulk_create(transaction_dtl_list)

            # Return all docno
            filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno').values_list('docno', flat=True)
            all_docno = list(filter_docno)
            return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)
        
    # book 3
    if exists_in_windows_book3:
            print('im book 3')
            print('3')
            is_iv_exists_windows_server_book3 = AcIV.objects.using('windows_server_book3').filter(docno=doc_no).first()
            sales_agent = is_iv_exists_windows_server_book3.salesagent
            
            display_term = Terms.objects.filter(displayterm=is_iv_exists_windows_server_book3.displayterm).first()
            doc_key = is_iv_exists_windows_server_book3.dockey
            invoice_date = is_iv_exists_windows_server_book3.docdate
            invoice_no = is_iv_exists_windows_server_book3.docno
            debtor_code_instsance = Debtor.objects.get(accno=is_iv_exists_windows_server_book3.debtorcode)
            debtor_code = is_iv_exists_windows_server_book3.debtorcode
            debtor_name = is_iv_exists_windows_server_book3.debtorname
            description = is_iv_exists_windows_server_book3.description
            total_invoice_amount = is_iv_exists_windows_server_book3.total
            currency_code = is_iv_exists_windows_server_book3.currencycode
            currency_rate = is_iv_exists_windows_server_book3.currencyrate
            post_to_stock = is_iv_exists_windows_server_book3.posttostock
            post_to_gl = is_iv_exists_windows_server_book3.posttogl
            transferable = is_iv_exists_windows_server_book3.transferable
            print_count = is_iv_exists_windows_server_book3.printcount
            last_modified = is_iv_exists_windows_server_book3.lastmodified
            lastmodifieduserid = is_iv_exists_windows_server_book3.lastmodifieduserid
            cancelled = is_iv_exists_windows_server_book3.cancelled
            created_time_stamp = is_iv_exists_windows_server_book3.createdtimestamp
            can_sync = is_iv_exists_windows_server_book3.cansync
            last_update = is_iv_exists_windows_server_book3.lastupdate
            reallocate_purchase_by_project = is_iv_exists_windows_server_book3.reallocatepurchasebyproject
            to_tax_currency_rate = is_iv_exists_windows_server_book3.totaxcurrencyrate
            rounding_method = is_iv_exists_windows_server_book3.roundingmethod
            location = Location.objects.get(location='NA') 

            ivdtl_windows_server = AcIVDTL.objects.using('windows_server_book3').filter(dockey=doc_key)
            item_code = AcIVDTL.objects.using('windows_server_book3').filter(dockey=doc_key).first().itemcode
            get_item_group_from_ivdtl = AcItem.objects.using('windows_server_book3').filter(itemcode=item_code).first().itemgroup

            if not sales_agent:
                sales_agent = SalesAgent.objects.get(salesagent='NA')
            else:
                sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            
            if get_item_group_from_ivdtl:
                filter_branch = Branch.objects.filter(address=get_item_group_from_ivdtl).first()
                if not filter_branch:
                    new_branch = Branch(address=get_item_group_from_ivdtl, companyautokey=tempcompanyautokey)
                    new_branch.save()

                    filter_branch = Branch.objects.get(address=get_item_group_from_ivdtl)
            else:
                filter_branch = Branch.objects.get(address='NA')
            # need to add lorry driver due to can't migrate
            new_iv = IV(udfbook='1',lorrydriver='NA',salesagent=sales_agent,displayterm=display_term,branchautokey=filter_branch,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code_instsance,debtorname=debtor_name,description=description,total=total_invoice_amount,nettotal=total_invoice_amount,localnettotal=total_invoice_amount,analysisnettotal=total_invoice_amount,finaltotal=total_invoice_amount,localtaxableamt=total_invoice_amount,taxcurrencytaxableamt=total_invoice_amount,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=last_modified,lastmodifieduserid=lastmodifieduserid,createdtimestamp=created_time_stamp,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
            new_transaction.save()

            get_iv_guid = IV.objects.get(docno=invoice_no)
            get_transaction_guid = Transaction.objects.filter(docno=invoice_no).first()
            
            ivdtl_list = []
            transaction_dtl_list = []
            
            for ivdtl in ivdtl_windows_server:
                if ivdtl.itemcode:

                    seq = ivdtl.seq
                    main_item = ivdtl.mainitem
                    item_code = ivdtl.itemcode
                    uom = ivdtl.uom
                    rate = ivdtl.rate
                    unit_price = ivdtl.unitprice
                    filter_itemcode = Item.objects.filter(itemcode=item_code).first()
                    if not filter_itemcode:
                        filter_windows_item = AcItem.objects.using('windows_server_book3').filter(itemcode=item_code).first()
                        item_brand = 'NA'
                        description = filter_windows_item.description
                        mainsupplier = 'book3'
                        last_modified = filter_windows_item.lastmodified
                        item_class = filter_windows_item.itemclass
                        

                        save_new_item = Item(itembrand=item_brand,itemcode=item_code,description=description,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=last_modified,lastupdate=0,itemclass=item_class)
                        save_new_item.save()

                        item_code_instance = Item.objects.get(itemcode = item_code)
                        
                        filter_windows_uom = AcItemUOM.objects.using('windows_server_book3').filter(itemcode=item_code).first()
                        udf_calmethod = filter_windows_uom.udfcalmethod
                        udf_calrate = filter_windows_uom.udfcalrate
                        # udf_pallet = filter_windows_uom.udfpallet
                        # , udfpallet=udf_pallet # add this
                        save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=item_code_instance,uom=uom,rate=rate,price=unit_price,lastupdate=0,udfcalmethod=udf_calmethod,udfcalrate=udf_calrate)
                        save_uom.save()
                    else:
                        filter_uom = ItemUOM.objects.filter(itemcode=item_code,uom=uom).first()
                        item_code_instance = Item.objects.get(itemcode = item_code)
                        if not filter_uom:
                            filter_windows_uom = AcItemUOM.objects.using('windows_server_book3').filter(itemcode=item_code).first()
                            udf_calmethod = filter_windows_uom.udfcalmethod
                            udf_calrate = filter_windows_uom.udfcalrate
                            # udf_pallet = filter_windows_uom.udfpallet
                            # , udfpallet=udf_pallet # add this
                            save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=item_code_instance,uom=uom,rate=rate,price=unit_price,lastupdate=0,udfcalmethod=udf_calmethod,udfcalrate=udf_calrate)
                            save_uom.save()
                    

                    quantity = ivdtl.qty
                    if not quantity:
                        quantity = ivdtl.focqty
                    smallest_qty = ivdtl.smallestqty
                    smallest_unit_price =ivdtl.smallestunitprice
                    net_amount = ivdtl.subtotal
                    description = ivdtl.description

                    item_class_value = item_code_instance.itemclass
                    item_code = item_code_instance.itemcode
                    # print(item_code,uom,quantity,rate,smallest_qty,unit_price,discount_amount,net_amount,description,item_class_value)
                    if not item_class_value:
                        # DELETE THE ADDED TRANSACTION HEADER
                        print('1')
                        new_iv.delete()
                        new_transaction.delete()
                        error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                        error['status'] = status.HTTP_404_NOT_FOUND
                        return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                    
                    item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                    comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                    new_ivdtl = IVDTL(autokey=panda_uuid(),guid=panda_uuid(),seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
                    ivdtl_list.append(new_ivdtl)
                    # new_ivdtl.save()
                    
                    new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=net_amount, uom=uom, commtype=comm_type)
                    transaction_dtl_list.append(new_transaction_dtl)
                    # new_transaction_dtl.save()

            with transaction.atomic():
                IVDTL.objects.bulk_create(ivdtl_list)
                TransactionDtl.objects.bulk_create(transaction_dtl_list)

            # Return all docno
            filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno').values_list('docno', flat=True)
            all_docno = list(filter_docno)
            return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)
    return

    if not is_iv_exists_in_ubuntu:
        is_iv_exists_book1 = AcIV.objects.using('windows_server').filter(docno=doc_no).exists()
# found in book 1
        if is_iv_exists_book1:
            is_iv_exists_windows_server = AcIV.objects.using('windows_server').filter(docno=doc_no).first()
            sales_agent = is_iv_exists_windows_server.salesagent
            
            display_term = Terms.objects.filter(displayterm=is_iv_exists_windows_server.displayterm).first()
            doc_key = is_iv_exists_windows_server.dockey
            invoice_date = is_iv_exists_windows_server.docdate
            invoice_no = is_iv_exists_windows_server.docno
            debtor_code_instsance = Debtor.objects.get(accno=is_iv_exists_windows_server.debtorcode)
            debtor_code = is_iv_exists_windows_server.debtorcode
            debtor_name = is_iv_exists_windows_server.debtorname
            description = is_iv_exists_windows_server.description
            total_invoice_amount = is_iv_exists_windows_server.total
            currency_code = is_iv_exists_windows_server.currencycode
            currency_rate = is_iv_exists_windows_server.currencyrate
            post_to_stock = is_iv_exists_windows_server.posttostock
            post_to_gl = is_iv_exists_windows_server.posttogl
            transferable = is_iv_exists_windows_server.transferable
            print_count = is_iv_exists_windows_server.printcount
            last_modified = is_iv_exists_windows_server.lastmodified
            lastmodifieduserid = is_iv_exists_windows_server.lastmodifieduserid
            cancelled = is_iv_exists_windows_server.cancelled
            created_time_stamp = is_iv_exists_windows_server.createdtimestamp
            can_sync = is_iv_exists_windows_server.cansync
            last_update = is_iv_exists_windows_server.lastupdate
            reallocate_purchase_by_project = is_iv_exists_windows_server.reallocatepurchasebyproject
            to_tax_currency_rate = is_iv_exists_windows_server.totaxcurrencyrate
            rounding_method = is_iv_exists_windows_server.roundingmethod
            location = Location.objects.get(location='NA') 

            ivdtl_windows_server = AcIVDTL.objects.using('windows_server').filter(dockey=doc_key)
            item_code = AcIVDTL.objects.using('windows_server').filter(dockey=doc_key).first().itemcode
            get_item_group_from_ivdtl = AcItem.objects.using('windows_server').filter(itemcode=item_code).first().itemgroup

            if not sales_agent:
                sales_agent = SalesAgent.objects.get(salesagent='NA')
            else:
                sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            
            if get_item_group_from_ivdtl:
                filter_branch = Branch.objects.filter(address=get_item_group_from_ivdtl).first()
                if not filter_branch:
                    new_branch = Branch(address=get_item_group_from_ivdtl, companyautokey=tempcompanyautokey)
                    new_branch.save()

                    filter_branch = Branch.objects.get(address=get_item_group_from_ivdtl)
            else:
                filter_branch = Branch.objects.get(address='NA')
            # need to add lorry driver due to can't migrate
            new_iv = IV(udfbook='1',lorrydriver='NA',salesagent=sales_agent,displayterm=display_term,branchautokey=filter_branch,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code_instsance,debtorname=debtor_name,description=description,total=total_invoice_amount,nettotal=total_invoice_amount,localnettotal=total_invoice_amount,analysisnettotal=total_invoice_amount,finaltotal=total_invoice_amount,localtaxableamt=total_invoice_amount,taxcurrencytaxableamt=total_invoice_amount,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=last_modified,lastmodifieduserid=lastmodifieduserid,createdtimestamp=created_time_stamp,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
            new_iv.save()

            new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
            new_transaction.save()

            get_iv_guid = IV.objects.get(docno=invoice_no)
            get_transaction_guid = Transaction.objects.filter(docno=invoice_no).first()
            
            ivdtl_list = []
            transaction_dtl_list = []
            
            for ivdtl in ivdtl_windows_server:
                if ivdtl.itemcode:

                    seq = ivdtl.seq
                    main_item = ivdtl.mainitem
                    item_code = ivdtl.itemcode
                    uom = ivdtl.uom
                    rate = ivdtl.rate
                    unit_price = ivdtl.unitprice
                    filter_itemcode = Item.objects.filter(itemcode=item_code).first()
                    if not filter_itemcode:
                        filter_windows_item = AcItem.objects.using('windows_server').filter(itemcode=item_code).first()
                        item_brand = 'NA'
                        description = filter_windows_item.description
                        mainsupplier = 'book1'
                        last_modified = filter_windows_item.lastmodified
                        item_class = filter_windows_item.itemclass
                        

                        save_new_item = Item(itembrand=item_brand,itemcode=item_code,description=description,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=last_modified,lastupdate=0,itemclass=item_class)
                        save_new_item.save()

                        item_code_instance = Item.objects.get(itemcode = item_code)
                        
                        filter_windows_uom = AcItemUOM.objects.using('windows_server').filter(itemcode=item_code).first()
                        udf_calmethod = filter_windows_uom.udfcalmethod
                        udf_calrate = filter_windows_uom.udfcalrate
                        # udf_pallet = filter_windows_uom.udfpallet
                        # , udfpallet=udf_pallet # add this
                        save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=item_code_instance,uom=uom,rate=rate,price=unit_price,lastupdate=0,udfcalmethod=udf_calmethod,udfcalrate=udf_calrate)
                        save_uom.save()
                    else:
                        filter_uom = ItemUOM.objects.filter(itemcode=item_code,uom=uom).first()
                        item_code_instance = Item.objects.get(itemcode = item_code)
                        if not filter_uom:
                            filter_windows_uom = AcItemUOM.objects.using('windows_server').filter(itemcode=item_code).first()
                            udf_calmethod = filter_windows_uom.udfcalmethod
                            udf_calrate = filter_windows_uom.udfcalrate
                            # udf_pallet = filter_windows_uom.udfpallet
                            # , udfpallet=udf_pallet # add this
                            save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=item_code_instance,uom=uom,rate=rate,price=unit_price,lastupdate=0,udfcalmethod=udf_calmethod,udfcalrate=udf_calrate)
                            save_uom.save()
                    

                    quantity = ivdtl.qty
                    if not quantity:
                        quantity = ivdtl.focqty
                    smallest_qty = ivdtl.smallestqty
                    smallest_unit_price =ivdtl.smallestunitprice
                    net_amount = ivdtl.subtotal
                    description = ivdtl.description

                    item_class_value = item_code_instance.itemclass
                    item_code = item_code_instance.itemcode
                    # print(item_code,uom,quantity,rate,smallest_qty,unit_price,discount_amount,net_amount,description,item_class_value)
                    if not item_class_value:
                        # DELETE THE ADDED TRANSACTION HEADER
                        print('1')
                        new_iv.delete()
                        new_transaction.delete()
                        error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                        error['status'] = status.HTTP_404_NOT_FOUND
                        return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                    
                    item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                    comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                    new_ivdtl = IVDTL(autokey=panda_uuid(),guid=panda_uuid(),seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
                    ivdtl_list.append(new_ivdtl)
                    # new_ivdtl.save()
                    
                    new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=net_amount, uom=uom, commtype=comm_type)
                    transaction_dtl_list.append(new_transaction_dtl)
                    # new_transaction_dtl.save()

            with transaction.atomic():
                IVDTL.objects.bulk_create(ivdtl_list)
                TransactionDtl.objects.bulk_create(transaction_dtl_list)

            # Return all docno
            filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno').values_list('docno', flat=True)
            all_docno = list(filter_docno)
            return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)
#         else:
# # found record in book 3
#             is_iv_exists_windows_server = AcIV.objects.using('windows_server_book3').filter(docno=doc_no).first()
#             sales_agent = is_iv_exists_windows_server.salesagent
            
#             display_term = Terms.objects.filter(displayterm=is_iv_exists_windows_server.displayterm).first()
#             doc_key = is_iv_exists_windows_server.dockey
#             invoice_date = is_iv_exists_windows_server.docdate
#             invoice_no = is_iv_exists_windows_server.docno
#             debtor_code_instsance = Debtor.objects.get(accno=is_iv_exists_windows_server.debtorcode)
#             debtor_code = is_iv_exists_windows_server.debtorcode
#             debtor_name = is_iv_exists_windows_server.debtorname
#             description = is_iv_exists_windows_server.description
#             total_invoice_amount = is_iv_exists_windows_server.total
#             currency_code = is_iv_exists_windows_server.currencycode
#             currency_rate = is_iv_exists_windows_server.currencyrate
#             post_to_stock = is_iv_exists_windows_server.posttostock
#             post_to_gl = is_iv_exists_windows_server.posttogl
#             transferable = is_iv_exists_windows_server.transferable
#             print_count = is_iv_exists_windows_server.printcount
#             last_modified = is_iv_exists_windows_server.lastmodified
#             lastmodifieduserid = is_iv_exists_windows_server.lastmodifieduserid
#             cancelled = is_iv_exists_windows_server.cancelled
#             created_time_stamp = is_iv_exists_windows_server.createdtimestamp
#             can_sync = is_iv_exists_windows_server.cansync
#             last_update = is_iv_exists_windows_server.lastupdate
#             reallocate_purchase_by_project = is_iv_exists_windows_server.reallocatepurchasebyproject
#             to_tax_currency_rate = is_iv_exists_windows_server.totaxcurrencyrate
#             rounding_method = is_iv_exists_windows_server.roundingmethod
#             location = Location.objects.get(location='NA') 

#             ivdtl_windows_server = AcIVDTL.objects.using('windows_server_book3').filter(dockey=doc_key)
#             item_code = AcIVDTL.objects.using('windows_server_book3').filter(dockey=doc_key).first().itemcode
#             get_item_group_from_ivdtl = AcItem.objects.using('windows_server_book3').filter(itemcode=item_code).first().itemgroup

#             if not sales_agent:
#                 sales_agent = SalesAgent.objects.get(salesagent='NA')
#             else:
#                 sales_agent = SalesAgent.objects.get(salesagent=sales_agent)
            
#             if get_item_group_from_ivdtl:
#                 filter_branch = Branch.objects.filter(address=get_item_group_from_ivdtl).first()
#                 if not filter_branch:
#                     new_branch = Branch(address=get_item_group_from_ivdtl, companyautokey=tempcompanyautokey)
#                     new_branch.save()

#                     filter_branch = Branch.objects.get(address=get_item_group_from_ivdtl)
#             else:
#                 filter_branch = Branch.objects.get(address='NA')
#             # need to add lorry driver due to can't migrate
#             new_iv = IV(udfbook='3',lorrydriver='NA',salesagent=sales_agent,displayterm=display_term,branchautokey=filter_branch,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code_instsance,debtorname=debtor_name,description=description,total=total_invoice_amount,nettotal=total_invoice_amount,localnettotal=total_invoice_amount,analysisnettotal=total_invoice_amount,finaltotal=total_invoice_amount,localtaxableamt=total_invoice_amount,taxcurrencytaxableamt=total_invoice_amount,currencycode=currency_code,currencyrate=currency_rate,posttostock=post_to_stock,posttogl=post_to_gl,transferable=transferable,printcount=print_count,cancelled=cancelled,lastmodified=last_modified,lastmodifieduserid=lastmodifieduserid,createdtimestamp=created_time_stamp,createduserid=lastmodifieduserid,cansync=can_sync,lastupdate=last_update,reallocatepurchasebyproject=reallocate_purchase_by_project, totaxcurrencyrate=to_tax_currency_rate,roundingmethod=rounding_method)
#             new_iv.save()

#             new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
#             new_transaction.save()

#             get_iv_guid = IV.objects.get(docno=invoice_no)
#             get_transaction_guid = Transaction.objects.filter(docno=invoice_no).first()
            
#             ivdtl_list = []
#             transaction_dtl_list = []
            
#             for ivdtl in ivdtl_windows_server:
#                 if ivdtl.itemcode:
#                     seq = ivdtl.seq
#                     main_item = ivdtl.mainitem
#                     item_code = ivdtl.itemcode
#                     item_code_instance = Item.objects.get(itemcode = item_code)
#                     uom = ivdtl.uom
#                     quantity = ivdtl.qty
#                     rate = ivdtl.rate
#                     smallest_qty = ivdtl.smallestqty
#                     rate = ivdtl.rate
#                     smallest_unit_price =ivdtl.smallestunitprice
#                     unit_price = ivdtl.unitprice
#                     discount_amount = ivdtl.discount
#                     net_amount = ivdtl.subtotal
#                     description = ivdtl.description
#                     # print(item_code)
#                     filter_item = Item.objects.filter(itemcode=item_code).first()
#                     item_class_value = filter_item.itemclass
#                     item_code = filter_item.itemcode
#                     if not item_class_value:
#                         # DELETE THE ADDED TRANSACTION HEADER
#                         print('1')
#                         new_iv.delete()
#                         new_transaction.delete()
#                         error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
#                         error['status'] = status.HTTP_404_NOT_FOUND
#                         return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                    
#                     item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
#                     comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
#                     new_ivdtl = IVDTL(autokey=panda_uuid(),guid=panda_uuid(),seq=seq,headerautokey=get_iv_guid,mainitem=main_item,itemcode=item_code_instance,description=description,uom=uom,useruom=uom,qty=quantity,rate=rate,smallestqty=smallest_qty,transferedqty=rate,smallestunitprice=smallest_unit_price,unitprice=unit_price,discount=discount_amount,discountamt=discount_amount,subtotal=net_amount,localsubtotal=net_amount,subtotalextax=net_amount,location=location,taxableamt=net_amount,localsubtotalextax=net_amount,localtaxableamt=net_amount,taxcurrencytaxableamt=net_amount)
#                     ivdtl_list.append(new_ivdtl)
#                     # new_ivdtl.save()
                    
#                     new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=total_invoice_amount, uom=uom, commtype=comm_type)
#                     transaction_dtl_list.append(new_transaction_dtl)
#                     # new_transaction_dtl.save()

#             with transaction.atomic():
#                 IVDTL.objects.bulk_create(ivdtl_list)
#                 TransactionDtl.objects.bulk_create(transaction_dtl_list)

#             # Return all docno
#             filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).values_list('docno', flat=True)
#             all_docno = list(filter_docno)
#             return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)
    else:
# found in django db
        filter_iv = IV.objects.filter(docno=doc_no).first()
        invoice_date = filter_iv.docdate
        invoice_no = filter_iv.docno
        debtor_code = filter_iv.debtorcode.accno
        debtor_name = filter_iv.debtorname
        transaction_dtl_list = []

        is_transaction_exists = Transaction.objects.filter(docno=invoice_no).exists()
        if not is_transaction_exists:
            new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
            new_transaction.save()
            get_transaction_guid = new_transaction
            iv = IV.objects.only("autokey").get(docno=invoice_no)
            filter_ivdtl = IVDTL.objects.filter(headerautokey=iv.autokey).only(
                "itemcode", "description", "qty", "subtotal", "uom"
            )
            
            for ivdtl in filter_ivdtl:
                if ivdtl.itemcode:
                    item_code = ivdtl.itemcode
                    description = ivdtl.description
                    quantity = ivdtl.qty
                    sub_total = ivdtl.subtotal
                    uom = ivdtl.uom
                    # print(item_code)
                    filter_item = Item.objects.filter(autokey=item_code).first()
                    item_class_value = filter_item.itemclass
                    item_code = filter_item.itemcode
                    if not item_class_value:
                        # DELETE THE ADDED TRANSACTION HEADER
                        print('2')
                        new_transaction.delete()
                        error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                        error['status'] = status.HTTP_404_NOT_FOUND
                        return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)
                    
                    item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                    
                    comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                    new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=sub_total, uom=uom, commtype=comm_type)
                    transaction_dtl_list.append(new_transaction_dtl)
                    # new_transaction_dtl.save()

            TransactionDtl.objects.bulk_create(transaction_dtl_list)
                    
            
            # Return all docno
            filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno').values_list('docno', flat=True)
            all_docno = list(filter_docno)
            return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)
        else:
            is_lorry_invoice_exists = Transaction.objects.filter(docno=invoice_no,lorryguid=lorry_guid)
            if not is_lorry_invoice_exists:
                new_transaction = Transaction(lorryguid=lorry_guid,docno=invoice_no,docdate=invoice_date,debtorcode=debtor_code,debtorname=debtor_name)
                new_transaction.save()
                get_transaction_guid = Transaction.objects.filter(docno=invoice_no).first()
                filter_ivdtl = IVDTL.objects.filter(headerautokey=IV.objects.get(docno=invoice_no).autokey)
                

                for ivdtl in filter_ivdtl:
                    if ivdtl.itemcode:
                        uom = ivdtl.uom
                        item_autokey = ivdtl.itemcode
                        item_code_instance = Item.objects.filter(autokey=item_autokey).first()
                        item_class_value = item_code_instance.itemclass
                        item_code = item_code_instance.itemcode
                        description = ivdtl.description
                        quantity = ivdtl.qty
                        sub_total = ivdtl.subtotal

                        if not item_class_value:
                            # DELETE THE ADDED TRANSACTION HEADER
                            print('3')
                            new_transaction.delete()
                            error['response'] = f'Item Class Not Found. ItemCode: {item_code}'
                            error['status'] = status.HTTP_404_NOT_FOUND
                            return JsonResponse(error, safe=False, status=status.HTTP_404_NOT_FOUND)

                        item_class = ItemClass.objects.prefetch_related('CommissionItemClassItemClassGuid').get(itemclass=item_class_value)
                        comm_type = item_class.CommissionItemClassItemClassGuid.first().commtype
                        new_transaction_dtl = TransactionDtl(transactiondtlguid=panda_uuid(),transactionguid=get_transaction_guid,itemclass=item_class, itemcode=item_code,description=description,qty=quantity,subtotal=sub_total,uom=uom, commtype=comm_type)
                        transaction_dtl_list.append(new_transaction_dtl)
                        
                TransactionDtl.objects.bulk_create(transaction_dtl_list)
                # Return all docno
                filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno')
                for docno in filter_docno:
                    all_docno.append(docno.docno)
                return JsonResponse(all_docno, safe=False, status=status.HTTP_201_CREATED)
            else:
                error['response'] = 'Invoice Exists For This Lorry'
                error['status'] = status.HTTP_409_CONFLICT
                return JsonResponse(error, safe=False, status=status.HTTP_409_CONFLICT)
    