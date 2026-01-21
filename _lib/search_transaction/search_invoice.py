from django.db import connection

def search_invoice(invoice_no):
    query_calculated_comm = """
        SELECT b.crewid, c.crewname, ROUND(SUM(CalculatedComm), 2) AS 'calculated comm', b.CrewGuid,
        e.DocDate, e.lorrynumber, e.lorryguid,
        ROUND(SUM(CASE WHEN a.CommType = %s THEN totalqty ELSE 0 END), 2) AS totalqty, 
        ROUND(SUM(CASE WHEN a.CommType = %s THEN totalamount ELSE 0 END), 2) AS totalamount
        FROM autocount_dashboard.crewdtl AS a
        INNER JOIN autocount_dashboard.crew AS b
            ON a.crewguid = b.crewguid
        INNER JOIN autocount_dashboard.crewrate AS c
            ON b.CrewId = c.crewid
        INNER JOIN autocount_dashboard.transaction AS d
            ON d.LorryGuid = b.LorryGuid
        INNER JOIN autocount_dashboard.lorry AS e
			ON d.lorryguid = e.lorryguid
        WHERE d.DocNo =%s
        GROUP BY b.crewid, b.CrewGuid
        ORDER BY b.crewid;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query_calculated_comm, ['$', '%',invoice_no])
        people_calculated_comm = cursor.fetchall() 
    
    all_calculated_comm = []

    for comm in people_calculated_comm:
        crew_id, crew_name, calculated_comm, crew_guid, doc_date, lorry_number, lorry_guid, total_qty, total_amount = comm
        crew_dtl = {'crewid': crew_id, 'crewname': crew_name, 'calculatedcomm': calculated_comm, "crewguid": crew_guid,'docdate': doc_date,'lorrynumber': lorry_number, 'lorry_guid':lorry_guid, 'totalqty': total_qty, 'totalamount': total_amount }
        all_calculated_comm.append(crew_dtl)

    return all_calculated_comm

        
    