from django.db import connection

def display_calculated_comm_by_lorryguid(lorryguid):

    # Query to count numbers of people in each lorry
    query_calculated_comm_by_lorryguid = """
        SELECT docno, lorryguid FROM autocount_dashboard.transaction
        WHERE LorryGuid=%s
        ORDER BY docno;
    """

    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(query_calculated_comm_by_lorryguid, [lorryguid])
        filter_calculated_comm_by_lorryguid = cursor.fetchall() 
    
    display_comm_by_lorryguid = []

    for comm in filter_calculated_comm_by_lorryguid:
        docno, lorry_guid = comm
        # crew_dtl = {'docno': docno, 'lorryguid': lorry_guid}
        display_comm_by_lorryguid.append(docno)

    return display_comm_by_lorryguid