from django.db import connection

def get_crew_details():

    # Query to count numbers of people in each lorry
    query_crew_details = """
        SELECT DISTINCT crewtype,crewid, crewname FROM autocount_dashboard.crewratedtl a
        INNER JOIN autocount_dashboard.crewrate b
        ON a.crewrateguid = b.CrewRateGuid
        ORDER BY crewid ASC;
    """

    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(query_crew_details)
        get_crew_details = cursor.fetchall() 
    
    crew_dict = {}
    
    for detail in get_crew_details:
        crew_type, crew_id, crew_name = detail
        
        # Check if this crew_id already exists in our dictionary
        if crew_id in crew_dict:
            # Update existing crew record based on crew_type
            if crew_type == 'Driver':
                crew_dict[crew_id]['isdriver'] = 1
            else:  # Assistant
                crew_dict[crew_id]['isassistant'] = 1
        else:
            # Create new crew record
            if crew_type == 'Driver':
                crew_dict[crew_id] = {
                    'crewid': crew_id,
                    'crewname': crew_name,
                    'isdriver': 1,
                    'isassistant': 0
                }
            else:  # Assistant
                crew_dict[crew_id] = {
                    'crewid': crew_id,
                    'crewname': crew_name,
                    'isdriver': 0,
                    'isassistant': 1
                }
    display_crew_details = list(crew_dict.values())
    
    return display_crew_details