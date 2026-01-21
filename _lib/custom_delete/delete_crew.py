from rest_framework import status
from django.http import JsonResponse
from crew.models import Crew
from crewrate.models import CrewRate
from crewdtl.models import Crewdtl

def delete_crew(lorry_guid,crew_id):
    is_crewid_exist = Crew.objects.filter(lorryguid=lorry_guid,crewid=crew_id).first()

    all_crew = []
    if is_crewid_exist:
        filter_crewdtl = Crewdtl.objects.filter(crewguid=is_crewid_exist.crewguid)
        
        if filter_crewdtl:
            filter_crewdtl.delete()
            
        is_crewid_exist.delete()

        filter_crew = Crew.objects.filter(lorryguid=lorry_guid)
        
        for doc in filter_crew:
            crew_id = doc.crewid
            crew_type = doc.crewtype
            filter_crew_rate = CrewRate.objects.filter(crewid=crew_id).first()
            crew_name = filter_crew_rate.crewname
            crew = {'crewid':crew_id,'crewname':crew_name,'crewtype':crew_type}
            all_crew.append(crew)
        
        return all_crew