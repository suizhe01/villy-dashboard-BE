from django.db import connection

def display_calculated_comm_by_crewguid(crew_guid):

    # Query to count numbers of people in each lorry
    query_calculated_comm_by_crewguid = """
        SELECT a.itemclass, ROUND(sum(totalqty), 2), ROUND(sum(TotalAmount), 2),a.commtype, a.commvalue, ROUND(SUM(a.calculatedcomm), 2)
        FROM autocount_dashboard.crewdtl AS a
        INNER JOIN autocount_dashboard.crew AS b
            ON a.crewguid = b.crewguid
        INNER JOIN autocount_dashboard.lorry AS d
            ON d.LorryGuid = b.LorryGuid
        WHERE a.crewguid = %s
        GROUP BY a.itemclass, a.commtype, a.commvalue
        ORDER BY ROUND(SUM(a.calculatedcomm), 2);
    """

    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(query_calculated_comm_by_crewguid, [crew_guid])
        filter_calculated_comm_by_crewguid = cursor.fetchall() 
    
    display_comm_by_crewguid = []

    for comm in filter_calculated_comm_by_crewguid:
        itemclass, sum_total_qty, sum_total_amount, comm_type, comm_value, calculated_comm = comm
        if comm_type == '%':
            sum_total_qty = 0
        elif comm_type == '$':
            sum_total_amount = 0
        crew_dtl = {'itemclass': itemclass, 'totalqty': sum_total_qty, 'totalamount': sum_total_amount, 'commtype': comm_type, 'commvalue': comm_value, 'calculatedcomm': calculated_comm}
        display_comm_by_crewguid.append(crew_dtl)

    return display_comm_by_crewguid