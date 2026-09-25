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

        
    

SEARCH_MIN_LENGTH = 3
SEARCH_MAX_INVOICES = 50

def search_invoices(query):
    """Find invoices whose number contains `query` (any case), across all dates.

    Returns one row per invoice x lorry x crew, newest lorry first, for at most
    SEARCH_MAX_INVOICES invoices. The commission on each row is that crew's
    total for the whole lorry trip; it is None when the lorry has not been
    calculated, and crewguid is None when the lorry has no crew registered.
    """
    q = (query or '').strip()
    if len(q) < SEARCH_MIN_LENGTH:
        return {'results': [], 'total_invoices': 0, 'shown_invoices': 0, 'too_short': True}

    # Whatever the user types is matched literally, so % and _ are not wildcards.
    pattern = '%' + q.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(DISTINCT d.DocNo)
            FROM autocount_dashboard.transaction AS d
            INNER JOIN autocount_dashboard.lorry AS e ON e.LorryGuid = d.LorryGuid
            WHERE d.DocNo LIKE %s
        """, [pattern])
        total_invoices = cursor.fetchone()[0]

        cursor.execute("""
            SELECT d.DocNo, MAX(e.DocDate) AS latest
            FROM autocount_dashboard.transaction AS d
            INNER JOIN autocount_dashboard.lorry AS e ON e.LorryGuid = d.LorryGuid
            WHERE d.DocNo LIKE %s
            GROUP BY d.DocNo
            ORDER BY latest DESC, d.DocNo
            LIMIT %s
        """, [pattern, SEARCH_MAX_INVOICES])
        doc_nos = [row[0] for row in cursor.fetchall()]

        if not doc_nos:
            return {'results': [], 'total_invoices': total_invoices, 'shown_invoices': 0, 'too_short': False}

        placeholders = ', '.join(['%s'] * len(doc_nos))
        # LEFT JOINs so a lorry without crew, or crew without a rate, still shows.
        cursor.execute(f"""
            SELECT d.DocNo, e.LorryGuid, e.LorryNumber, e.DocDate, b.CrewGuid, b.CrewId, c.CrewName
            FROM autocount_dashboard.transaction AS d
            INNER JOIN autocount_dashboard.lorry AS e ON e.LorryGuid = d.LorryGuid
            LEFT JOIN autocount_dashboard.crew AS b ON b.LorryGuid = e.LorryGuid
            LEFT JOIN autocount_dashboard.crewrate AS c ON c.CrewId = b.CrewId
            WHERE d.DocNo IN ({placeholders})
            ORDER BY e.DocDate DESC, d.DocNo, c.CrewName, b.CrewId
        """, doc_nos)
        rows = cursor.fetchall()

        # Summed per crew on its own, not joined to the matching invoices: a
        # lorry carrying two matching invoices would otherwise count twice.
        crew_guids = sorted({row[4] for row in rows if row[4]})
        totals = {}
        if crew_guids:
            placeholders = ', '.join(['%s'] * len(crew_guids))
            cursor.execute(f"""
                SELECT CrewGuid, ROUND(SUM(CalculatedComm), 2),
                       ROUND(SUM(CASE WHEN CommType = %s THEN TotalQty ELSE 0 END), 2),
                       ROUND(SUM(CASE WHEN CommType = %s THEN TotalAmount ELSE 0 END), 2)
                FROM autocount_dashboard.crewdtl
                WHERE CrewGuid IN ({placeholders})
                GROUP BY CrewGuid
            """, ['$', '%'] + crew_guids)
            totals = {row[0]: row[1:] for row in cursor.fetchall()}

    results = []
    for doc_no, lorry_guid, lorry_number, doc_date, crew_guid, crew_id, crew_name in rows:
        calculated_comm, total_qty, total_amount = totals.get(crew_guid, (None, None, None))
        results.append({
            'docno': doc_no,
            'crewid': crew_id,
            'crewname': crew_name or crew_id,
            'calculatedcomm': calculated_comm,
            'crewguid': crew_guid,
            'docdate': doc_date,
            'lorrynumber': lorry_number,
            'lorry_guid': lorry_guid,
            'totalqty': total_qty,
            'totalamount': total_amount,
        })

    return {'results': results, 'total_invoices': total_invoices, 'shown_invoices': len(doc_nos), 'too_short': False}
