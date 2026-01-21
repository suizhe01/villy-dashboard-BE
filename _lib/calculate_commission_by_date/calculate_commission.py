from lorry.models import Lorry
from crew.models import Crew
from crewdtl.models import Crewdtl
from django.db import connection
from datetime import datetime
from transaction.models import Transaction
from transactiondtl.models import TransactionDtl
from itemclass.models import ItemClass
from _lib.panda import panda_uuid
from itemuom.models import ItemUOM
from item.models import Item
from decimal import Decimal

def flag_share_value(start_date, end_date):
    flag_1_query = """
        SELECT a.docno FROM autocount_dashboard.transaction AS a
        INNER JOIN autocount_dashboard.lorry AS b
            ON a.lorryguid = b.lorryguid
            WHERE b.docdate BETWEEN %s AND %s
        GROUP BY a.DocNo
        HAVING COUNT(a.DocNo) = 1;
    """

    # Use parameterized queries to avoid SQL injection
    with connection.cursor() as cursor:
        cursor.execute(flag_1_query, [start_date, end_date])
        results = cursor.fetchall()
    
    for result in results:
        doc_no = result[0]
        multiple_transaction = Transaction.objects.filter(docno=doc_no)
        for transaction in multiple_transaction:
            if transaction.share != 1:
                transaction.share = 1
                transaction.save()

    flag_2_query = """
        SELECT a.docno FROM autocount_dashboard.transaction AS a
        INNER JOIN autocount_dashboard.lorry AS b
            ON a.lorryguid = b.lorryguid
            WHERE b.docdate BETWEEN %s AND %s
        GROUP BY a.DocNo
        HAVING COUNT(a.DocNo) = 2;
    """

    # Use parameterized queries to avoid SQL injection
    with connection.cursor() as cursor:
        cursor.execute(flag_2_query, [start_date, end_date])
        results = cursor.fetchall()
    
    for result in results:
        doc_no = result[0]
        multiple_transaction = Transaction.objects.filter(docno=doc_no)
        for transaction in multiple_transaction:
            if transaction.share != 2:
                transaction.share = 2
                transaction.save()

    flag_3_query = """
        SELECT a.docno FROM autocount_dashboard.transaction AS a
        INNER JOIN autocount_dashboard.lorry AS b
            ON a.lorryguid = b.lorryguid
            WHERE b.docdate BETWEEN %s AND %s
        GROUP BY a.DocNo
        HAVING COUNT(a.DocNo) = 3;
    """

    # Use parameterized queries to avoid SQL injection
    with connection.cursor() as cursor:
        cursor.execute(flag_3_query, [start_date, end_date])
        results = cursor.fetchall()
    
    for result in results:
        doc_no = result[0]
        multiple_transaction = Transaction.objects.filter(docno=doc_no)
        for transaction in multiple_transaction:
            if transaction.share != 3:
                transaction.share = 3
                transaction.save()

def update_transactiondtl_calmethod_calrate(start_date, end_date):
    filter_cal_method_not_null =ItemUOM.objects.filter(udfcalmethod__isnull=False).values_list('itemcode', 'uom','udfcalmethod','udfcalrate')
    item_udf = {(item[0], item[1]): (item[2], item[3]) for item in filter_cal_method_not_null}

    query_for_transactiondtl = """
    SELECT a.transactiondtlguid ,a.itemcode, a.uom, a.UdfCalMethod
    FROM autocount_dashboard.transactiondtl AS a
    INNER JOIN autocount_dashboard.transaction AS b
        ON a.transactionguid = b.TransactionGuid
    INNER JOIN autocount_dashboard.lorry AS c
        on b.lorryguid = c.lorryguid
    INNER JOIN autocount_dashboard.itemclass AS d
        on a.itemclass = d.itemclass
    INNER JOIN autocount_dashboard.commissionitemclass AS e
        on d.itemclassguid = e.itemclassguid
    WHERE c.docdate BETWEEN %s AND %s;
    """
    bulk_update_commtype = []
    # Use parameterized queries to avoid SQL injection
    with connection.cursor() as cursor:
        cursor.execute(query_for_transactiondtl, [start_date, end_date])
        update_commtype = cursor.fetchall()

    for update in update_commtype:
        transactiondtl_guid = update[0]
        item_code = update[1]
        uom = update[2]
        udf_calmethod = update[3]

        key = (item_code, uom)
        if key in item_udf:
            if not udf_calmethod:
                print('im neww')
                udf_calmethod,udf_calrate = item_udf[key]
                bulk_update_commtype.append((transactiondtl_guid,udf_calmethod,udf_calrate))

    for transactiondtl_guid,udf_calmethod,udf_calrate in bulk_update_commtype:
            TransactionDtl.objects.filter(transactiondtlguid=transactiondtl_guid).update(udfcalmethod=udf_calmethod, udfcalrate=udf_calrate)

def update_transaction_debtor_is_pallet(start_date, end_date):
    query = """
    SELECT a.TransactionGuid
    FROM autocount_dashboard.transaction AS a
    INNER JOIN autocount_dashboard.lorry AS b
        ON a.LorryGuid = b.LorryGuid
    WHERE a.DebtorCode IN (SELECT accno FROM autocount_dashboard.debtor
    where udfispallet>'0') 
    AND b.DocDate BETWEEN %s AND %s
    AND a.UdfIsPallet < '1';
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date])
        update_is_pallet = cursor.fetchall()

    update_new_is_pallet = []
    if update_is_pallet:
        for pallet in update_is_pallet:
            transactionguid = pallet[0]
            update_new_is_pallet.append((transactionguid))

    if update_new_is_pallet:      
        for transactionguid in update_new_is_pallet:
            Transaction.objects.filter(transactionguid=transactionguid).update(udfispallet=1)

def update_transactiondtl_item_ispallet(start_date, end_date):
    query = """
    SELECT a.transactiondtlguid
    FROM autocount_dashboard.transactiondtl AS a
    INNER JOIN autocount_dashboard.transaction AS b
        ON a.transactionguid = b.TransactionGuid
    INNER JOIN autocount_dashboard.lorry AS c
        on b.lorryguid = c.lorryguid
    WHERE c.docdate BETWEEN %s AND %s
    AND a.ItemCode IN (SELECT itemcode FROM autocount_dashboard.itemuom
    WHERE UdfPallet>0);
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date])
        update_ispallet = cursor.fetchall()

    update_transactiondtl_ispallet = []
    if update_ispallet:
        for pallet in update_ispallet:
            transactiondtlguid = pallet[0]
            update_transactiondtl_ispallet.append((transactiondtlguid))
    
    if update_transactiondtl_ispallet:
        for transactiondtlguid in update_transactiondtl_ispallet:
            TransactionDtl.objects.filter(transactiondtlguid=transactiondtlguid).update(udfispallet=1)

def update_transactiondtl_ispallet_itemclass(start_date, end_date):
    query = """
    SELECT TransactionDtlGuid
    FROM autocount_dashboard.transactiondtl AS a
    INNER JOIN autocount_dashboard.transaction AS b
        ON a.transactionguid = b.TransactionGuid
    INNER JOIN autocount_dashboard.lorry AS c
        on b.lorryguid = c.lorryguid
    WHERE c.docdate BETWEEN %s AND %s
    AND b.UdfIsPallet>'0' AND a.UdfIsPallet >'0';
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date])
        update_ispallet_itemclass = cursor.fetchall()

    update_transactiondtl_ispallet_itemclass = []
    if update_ispallet_itemclass:
        for pallet in update_ispallet_itemclass:
            transactiondtlguid = pallet[0]
            update_transactiondtl_ispallet_itemclass.append((transactiondtlguid))
    
    if update_transactiondtl_ispallet_itemclass:
        for transactiondtlguid in update_transactiondtl_ispallet_itemclass:
            TransactionDtl.objects.filter(transactiondtlguid=transactiondtlguid).update(itemclass='RB PALLET(Q)')

def update_transactiondtl_qty(start_date, end_date):
    query = """
    SELECT a.TransactionDtlGuid ,a.UdfCalMethod, a.UdfCalRate, qty, a.isqtyupdated, a.uom, a.itemclass
    FROM autocount_dashboard.transactiondtl AS a
    INNER JOIN autocount_dashboard.transaction AS b
        ON a.transactionguid = b.TransactionGuid
    INNER JOIN autocount_dashboard.lorry AS c
        on b.lorryguid = c.lorryguid
    WHERE c.docdate BETWEEN %s AND %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date])
        update_qty = cursor.fetchall()
    
    update_new_qty = []
    for update in update_qty:
        transactiondtl_guid, udf_calmethod, udf_calrate, qty, isqty_updated, uom, itemclass = update
        if itemclass=='SUNQUICK(Q)':
            if uom == 'UNT':
                print('hi')
                new_qty = qty/6
                update_new_qty.append((transactiondtl_guid,new_qty))

        if isqty_updated == 0:
            if udf_calmethod:
                new_qty = qty*udf_calrate
                update_new_qty.append((transactiondtl_guid,new_qty))

    for transactiondtl_guid,new_qty in update_new_qty:
            TransactionDtl.objects.filter(transactiondtlguid=transactiondtl_guid).update(qty=new_qty,isqtyupdated=1)

def delete_crewdtl(start_date, end_date):
    # Query to delete crew details first before add
    query_delete_crew_commission_dtl = """
    DELETE FROM autocount_dashboard.crewdtl
    WHERE CrewDtlGuid IN (
        SELECT crewdtlguid FROM (
            SELECT a.crewdtlguid
            FROM autocount_dashboard.crewdtl AS a
            INNER JOIN autocount_dashboard.crew AS b
                ON a.CrewGuid = b.CrewGuid
            INNER JOIN autocount_dashboard.lorry AS c
                ON b.LorryGuid = c.LorryGuid
            WHERE c.DocDate BETWEEN %s AND %s
        ) AS temp_table
    );
    """

    with connection.cursor() as cursor:
        cursor.execute(query_delete_crew_commission_dtl, [start_date, end_date])

def create_crewdtl(start_date, end_date):
    query_add_crewdtl = """
        SELECT itemclass,SUM(qty), sum(SubTotal), c.lorryguid, b.share, a.UdfCalMethod, a.UdfCalRate,a.CommType
        FROM autocount_dashboard.transactiondtl AS a
        INNER JOIN autocount_dashboard.transaction AS b
            ON a.transactionguid = b.TransactionGuid
        INNER JOIN autocount_dashboard.lorry AS c
            on b.lorryguid = c.lorryguid
        WHERE c.docdate BETWEEN %s AND %s
        AND NOT (a.subtotal <= 0 AND itemclass NOT IN ('SUNQUICK(Q)', 'SUNDRY($)', 'CHEERS(Q)'))
        GROUP BY b.Share,a.itemclass, c.lorryguid, a.UdfCalMethod, a.UdfCalRate, a.CommType;
    """

    add_new_crewdtl = []
    # Use parameterized queries to avoid SQL injection
    with connection.cursor() as cursor:
        cursor.execute(query_add_crewdtl, [start_date, end_date])
        crewdtl_results = cursor.fetchall()
    
    for result in crewdtl_results:
        # uom = result[0]
        item_class = result[0]
        total_qty = result[1]
        total_amount = result[2]
        lorry_guid = result[3]
        share = result[4]
        udf_calmethod = result[5]
        udf_calrate = result[6]
        comm_type = result[7]

        if item_class != 'SUNQUICK(Q)' and item_class != 'CHEERS(Q)':
            if total_amount > 0:
                # print(item_class)

                filter_crew = Crew.objects.filter(lorryguid=lorry_guid)
                if filter_crew:
                    for crew in filter_crew:
                        crew_guid = crew.crewguid
                        filter_crewdtl = Crewdtl.objects.filter(crewguid=crew_guid,itemclass=item_class)
                        if not filter_crewdtl:
                            crewguid_instance = Crew.objects.get(crewguid=crew_guid)
                            item_class_instance = ItemClass.objects.get(itemclass=item_class)
                            new_crewdtl = Crewdtl(crewdtlguid=panda_uuid(),crewguid=crewguid_instance, itemclass=item_class_instance,totalqty=total_qty,totalamount=total_amount,share=share,udfcalmethod=udf_calmethod, udfcalrate=udf_calrate, commtype=comm_type)
                            add_new_crewdtl.append(new_crewdtl)
                            # print(lorry_guid,crew_guid)
        else:
            # print(item_class)
            filter_crew = Crew.objects.filter(lorryguid=lorry_guid)
            if filter_crew:
                for crew in filter_crew:
                    crew_guid = crew.crewguid
                    filter_crewdtl = Crewdtl.objects.filter(crewguid=crew_guid,itemclass=item_class)
                    if not filter_crewdtl:
                        crewguid_instance = Crew.objects.get(crewguid=crew_guid)
                        item_class_instance = ItemClass.objects.get(itemclass=item_class)
                        new_crewdtl = Crewdtl(crewdtlguid=panda_uuid(),crewguid=crewguid_instance, itemclass=item_class_instance,totalqty=total_qty,totalamount=total_amount,share=share,udfcalmethod=udf_calmethod, udfcalrate=udf_calrate, commtype=comm_type)
                        add_new_crewdtl.append(new_crewdtl)
                        
    if add_new_crewdtl:           
        Crewdtl.objects.bulk_create(add_new_crewdtl)

def update_crewdtl_commvalue(start_date, end_date):
    # Query to get crew details
    query_crew_commission_dtl = """
    SELECT crewid, crewtype, crewdtlguid, itemclass 
    FROM autocount_dashboard.crewdtl AS a
    INNER JOIN autocount_dashboard.crew AS b
        ON a.crewguid = b.crewguid
    INNER JOIN autocount_dashboard.lorry AS c
        ON c.LorryGuid = b.LorryGuid
    WHERE c.DocDate BETWEEN %s AND %s;
    """

    # Query to get crew rate details
    query_crewrate = """
        SELECT crewid,crewtype, itemclass, crewname, isactive,  commvalue
        FROM autocount_dashboard.crewratedtl AS a
        INNER JOIN autocount_dashboard.crewrate AS b
            ON a.CrewRateGuid = b.CrewRateGuid
        INNER JOIN autocount_dashboard.commissionitemclass AS c
            ON c.commissionitemclassguid = a.commissionitemclassguid
        INNER JOIN autocount_dashboard.itemclass AS d
            ON d.itemclassguid = c.itemclassguid
        ORDER BY b.CrewName ASC;
    """

    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(query_crew_commission_dtl, [start_date, end_date])
        crewdtl_added_table = cursor.fetchall()  

        cursor.execute(query_crewrate)
        crewratedtl_table = cursor.fetchall() 

    crewratedtl_dict = {(item[0], item[1], item[2] ): (item[3],item[4],item[5]) for item in crewratedtl_table}
    
    update_crewdtl = []
    # print(crewratedtl_dict)
    test = []
    for crewdtl in crewdtl_added_table:
        crewid, crewtype, crewdtl_guid, itemclass = crewdtl
        # print(crewid,crewtype,itemclass)
        key = (crewid,crewtype, itemclass)
        if key in crewratedtl_dict:
            crewname, isactive,  comm_value = crewratedtl_dict[key]
            update_crewdtl.append((crewdtl_guid,comm_value))

    for crewdtl_guid,comm_value in update_crewdtl:
            Crewdtl.objects.filter(crewdtlguid=crewdtl_guid).update(commvalue=comm_value)

def calculation_for_document_sum(start_date, end_date):
    # Query to count numbers of people in each lorry
    query_people_in_lorry = """
        SELECT a.lorryguid, COUNT(*) AS people
        FROM autocount_dashboard.lorry AS a
        INNER JOIN autocount_dashboard.crew AS b
            ON a.lorryguid = b.lorryguid
        WHERE a.DocDate BETWEEN %s AND %s
        GROUP BY a.lorryguid;
    """

    # Query to get crewdtl value for calculation
    query_crewdtl_calculation = """
        SELECT crewdtlguid, commtype, commvalue, totalamount, totalqty, share, b.lorryguid, a.calculatedcomm
        FROM autocount_dashboard.crewdtl AS a
        INNER JOIN autocount_dashboard.crew AS b
            ON a.crewguid = b.CrewGuid
        INNER JOIN autocount_dashboard.lorry AS c
            ON b.LorryGuid = c.lorryguid
        WHERE c.DocDate BETWEEN %s AND %s;
    """

    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(query_people_in_lorry, [start_date, end_date])
        people_in_lorry_table = cursor.fetchall()  

        cursor.execute(query_crewdtl_calculation, [start_date, end_date])
        crewdtl_calculation_table = cursor.fetchall()  

    people_dict = {item[0]: (item[1]) for item in people_in_lorry_table}
    
    update_calculated_comm = []
    for crewdtl in crewdtl_calculation_table:
        crewdtlguid, commtype, commvalue, totalamount, totalqty, share, lorryguid, calculatedcomm = crewdtl

        number_of_people_in_lorry = people_dict[lorryguid]
        if not calculatedcomm:
            if share == 1:
                if number_of_people_in_lorry <= 2:
                    if commtype == '%':
                        if not commvalue:
                            print(crewdtlguid)
                        calculated_comm = round((commvalue * totalamount),2)
                        update_calculated_comm.append((crewdtlguid,calculated_comm,totalamount,totalqty))
                    else:
                        if not commvalue:
                            print(crewdtlguid)
                        calculated_comm = commvalue * totalqty
                        update_calculated_comm.append((crewdtlguid,calculated_comm,totalamount,totalqty))
                elif number_of_people_in_lorry == 3:
                    totalamount = ((totalamount*2)/3)
                    # if lorryguid == :
                    totalqty = ((totalqty*2)/3)
                    if commtype == '%':
                        calculated_comm = round((commvalue * totalamount),2)
                        update_calculated_comm.append((crewdtlguid,calculated_comm,totalamount,totalqty))
                    else:
                        calculated_comm = commvalue * totalqty
                        update_calculated_comm.append((crewdtlguid,calculated_comm,totalamount,totalqty))
            elif share == 2:
                if number_of_people_in_lorry == 2:
                    totalamount = round((totalamount/2), 2)
                    totalqty = totalqty/2
                    if commtype == '%':
                        calculated_comm = round((commvalue * totalamount),2)
                        update_calculated_comm.append((crewdtlguid,calculated_comm,totalamount,totalqty))
                    else:
                        calculated_comm = commvalue * totalqty
                        update_calculated_comm.append((crewdtlguid,calculated_comm,totalamount,totalqty))
            elif share == 3:
                if number_of_people_in_lorry == 2:
                    totalamount = round(((totalamount*2)/6), 2)
                    totalqty = ((totalqty*2)/6)
                    if commtype == '%':
                        calculated_comm = round((commvalue * totalamount),2)
                        update_calculated_comm.append((crewdtlguid,calculated_comm,totalamount,totalqty))
                    else:
                        calculated_comm = commvalue * totalqty
                        update_calculated_comm.append((crewdtlguid,calculated_comm,totalamount,totalqty))

    for crewdtl_guid,calculated_comm,totalamount,totalqty in update_calculated_comm:
        calculated_comm = Decimal(calculated_comm).quantize(Decimal('0.01'))
        # calculated_comm = round(calculated_comm,2)
        # print(calculated_comm)
        Crewdtl.objects.filter(crewdtlguid=crewdtl_guid).update(calculatedcomm=calculated_comm, totalamount=totalamount,totalqty=totalqty)

def display_calculated_comm(start_date, end_date):
    # Query to count numbers of people in each lorry
    query_calculated_comm = """
        SELECT b.crewid, c.crewname, ROUND(SUM(CalculatedComm), 2) AS 'calculated comm'
        FROM autocount_dashboard.crewdtl AS a
        INNER JOIN autocount_dashboard.crew AS b
            ON a.crewguid = b.crewguid
        INNER JOIN autocount_dashboard.crewrate AS c
            ON b.CrewId = c.crewid
        INNER JOIN autocount_dashboard.lorry AS d
            ON d.LorryGuid = b.LorryGuid
        WHERE d.docdate BETWEEN %s AND %s
        GROUP BY b.crewid
        ORDER BY b.crewid;
    """

    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(query_calculated_comm, [start_date, end_date])
        people_calculated_comm = cursor.fetchall() 
    
    all_calculated_comm = []

    for comm in people_calculated_comm:
        crew_id, crew_name, calculated_comm = comm
        crew_dtl = {'crewid': crew_id, 'crewname': crew_name, 'calculatedcomm': calculated_comm}
        all_calculated_comm.append(crew_dtl)
    
    return all_calculated_comm

def calculate_commission_by_date(start_date, end_date,tempcompanyautokey):
    # # # flag 1/2 for share
    flag_share_value(start_date, end_date)
    
    # update transactiondtl for calmethod and calrate 
    update_transactiondtl_calmethod_calrate(start_date, end_date)

    update_transactiondtl_qty(start_date,end_date)

    update_transaction_debtor_is_pallet(start_date, end_date)

    update_transactiondtl_item_ispallet(start_date,end_date)

    update_transactiondtl_ispallet_itemclass(start_date,end_date)

    delete_crewdtl(start_date, end_date)

    create_crewdtl(start_date, end_date)
    
    update_crewdtl_commvalue(start_date, end_date)

    calculation_for_document_sum(start_date, end_date)

    return display_calculated_comm(start_date,end_date)

    

