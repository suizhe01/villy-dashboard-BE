from rest_framework import status
from django.http import JsonResponse
from crew.models import Crew
from crewrate.models import CrewRate

def create_crew(lorry_guid,crew_id,crew_type):
    if not crew_id or not crew_type:
        all_crew = []
        # Return all docno
        filter_crew = Crew.objects.filter(lorryguid=lorry_guid)
        # all_crew = list(filter_crew)
        for doc in filter_crew:
            crew_id = doc.crewid
            crew_type = doc.crewtype
            filter_crew_rate = CrewRate.objects.filter(crewid=crew_id).first()
            crew_name = filter_crew_rate.crewname
            crew = {'crewid':crew_id,'crewname':crew_name,'crewtype':crew_type}
            all_crew.append(crew)
        return all_crew

    is_crewid_exist = Crew.objects.filter(lorryguid=lorry_guid,crewid=crew_id).exists()

    if not is_crewid_exist:
        new_crew = Crew(lorryguid=lorry_guid,crewid=crew_id,crewtype=crew_type)
        new_crew.save()


    all_crew = []
    # Return all docno
    filter_crew = Crew.objects.filter(lorryguid=lorry_guid)
    # all_crew = list(filter_crew)
    for doc in filter_crew:
        crew_id = doc.crewid
        crew_type = doc.crewtype
        filter_crew_rate = CrewRate.objects.filter(crewid=crew_id).first()
        crew_name = filter_crew_rate.crewname
        crew = {'crewid':crew_id,'crewname':crew_name,'crewtype':crew_type}
        all_crew.append(crew)
    return all_crew
    print(all_crew, filter_crew)
    return JsonResponse(all_crew, safe=False, status=status.HTTP_201_CREATED)