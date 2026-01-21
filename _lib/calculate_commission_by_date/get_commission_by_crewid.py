from django.db import connection

def display_calculated_comm_by_crewid(start_date, end_date, crew_id):

    # Query to count numbers of people in each lorry
    query_calculated_comm_by_crewid = """
        SELECT d.docdate,d.lorrynumber, b.crewid, c.crewname, ROUND(SUM(CalculatedComm), 2) AS calculated_comm, 
        ROUND(SUM(CASE WHEN a.CommType = %s THEN totalqty ELSE 0 END), 2) AS totalqty, 
        ROUND(SUM(CASE WHEN a.CommType = %s THEN totalamount ELSE 0 END), 2) AS totalamount,  
        b.CrewGuid, b.LorryGuid
        FROM autocount_dashboard.crewdtl AS a
        INNER JOIN autocount_dashboard.crew AS b
            ON a.crewguid = b.crewguid
        INNER JOIN autocount_dashboard.crewrate AS c
            ON b.CrewId = c.crewid
        INNER JOIN autocount_dashboard.lorry AS d
            ON d.LorryGuid = b.LorryGuid
        WHERE d.docdate BETWEEN %s AND %s
        AND b.crewid = %s
        GROUP BY b.crewid,b.CrewGuid
        ORDER BY d.docdate;
    """

    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(query_calculated_comm_by_crewid, ['$', '%', start_date, end_date, crew_id])
        filter_calculated_comm_by_crewid = cursor.fetchall() 
    
    display_comm_by_crewid = []

    for comm in filter_calculated_comm_by_crewid:
        doc_date, lorry_number, crew_id,crew_name,calculated_comm, total_qty, total_amount, crew_guid, lorry_guid = comm
        crew_dtl = {'docdate': doc_date,'lorrynumber': lorry_number ,'crewid': crew_id, 'crewname': crew_name, 'calculatedcomm': calculated_comm, 'crewguid':crew_guid, 'lorry_guid':lorry_guid, 'totalqty': total_qty, 'totalamount': total_amount}
        display_comm_by_crewid.append(crew_dtl)
        

    return display_comm_by_crewid