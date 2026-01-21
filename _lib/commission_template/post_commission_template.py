from crewrate.models import CrewRate
from crewratedtl.models import CrewRateDtl
from django.db import transaction
from _lib.panda import panda_uuid
from lorryplate.models import LorryPlate

def post_commission_template(employee_id,crew_name, crew_type,car_plate, sundry_m,dob_m,rb_q,yltc_q,le_q,cheers_q,rbpallet_q,sajioil_q,sajioilpallet_q,sajisweet_q,sajisweetpallet_q,dutchlady_m,lipton_m,mamee_m,mamypoko_m,dksh_m,sunquick_q,filter_sundry_m,filter_dob_m,filter_rb_q,filter_yltc_q,filter_le_q,filter_cheers_q,filter_rbpallet_q,filter_sajioil_q,filter_sajioilpallet_q,filter_sajisweet_q,filter_sajisweetpallet_q,filter_dutchlady_m,filter_lipton_m,filter_mamee_m,filter_mamypoko_m,filter_dksh_m,filter_sunquick_q):
    filter_lorry_plate = LorryPlate.objects.filter(lorrynumber=car_plate)
    if not filter_lorry_plate:
        new_lorry_plate = LorryPlate(lorrynumber=car_plate)
        new_lorry_plate.save()
    # filter_crewrate_crewname = CrewRate.objects.filter(crewid=employee_id)
    
    # if not filter_crewrate_crewname:
    create_crewrate = CrewRate(crewid=employee_id,crewname=crew_name,isactive=1)
    create_crewrate.save()
        
    get_crewrateguid = CrewRate.objects.get(crewid=employee_id)

    # filter_crewratedtl = CrewRateDtl.objects.filter(crewrateguid=get_crewrateguid, crewtype=crew_type)
    # if filter_crewratedtl:
    #     filter_crewratedtl.delete()
    

    add_crewratedtl_sundry_m = CrewRateDtl(commissionitemclassguid=filter_sundry_m,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=sundry_m)
    add_crewratedtl_sundry_m.save()

    add_crewratedtl_dob_m = CrewRateDtl(commissionitemclassguid=filter_dob_m,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=dob_m)
    add_crewratedtl_dob_m.save()

    add_crewratedtl_rb_q = CrewRateDtl(commissionitemclassguid=filter_rb_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=rb_q)
    add_crewratedtl_rb_q.save()

    add_crewratedtl_yltc_q = CrewRateDtl(commissionitemclassguid=filter_yltc_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=yltc_q)
    add_crewratedtl_yltc_q.save()

    add_crewratedtl_le_q = CrewRateDtl(commissionitemclassguid=filter_le_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=le_q)
    add_crewratedtl_le_q.save()
    
    add_crewratedtl_cheers_q = CrewRateDtl(commissionitemclassguid=filter_cheers_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=cheers_q)
    add_crewratedtl_cheers_q.save()
    
    add_crewratedtl_rbpallet_q = CrewRateDtl(commissionitemclassguid=filter_rbpallet_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=rbpallet_q)
    add_crewratedtl_rbpallet_q.save()
    
    add_crewratedtl_sajioil_q = CrewRateDtl(commissionitemclassguid=filter_sajioil_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=sajioil_q)
    add_crewratedtl_sajioil_q.save()
    
    add_crewratedtl_sajioilpallet_q = CrewRateDtl(commissionitemclassguid=filter_sajioilpallet_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=sajioilpallet_q)
    add_crewratedtl_sajioilpallet_q.save()

    add_crewratedtl_sajisweet_q = CrewRateDtl(commissionitemclassguid=filter_sajisweet_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=sajisweet_q)
    add_crewratedtl_sajisweet_q.save()

    add_crewratedtl_sajisweetpallet_q = CrewRateDtl(commissionitemclassguid=filter_sajisweetpallet_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=sajisweetpallet_q)
    add_crewratedtl_sajisweetpallet_q.save()

    add_crewratedtl_dutchlady_m = CrewRateDtl(commissionitemclassguid=filter_dutchlady_m,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=dutchlady_m)
    add_crewratedtl_dutchlady_m.save()

    add_crewratedtl_lipton_m = CrewRateDtl(commissionitemclassguid=filter_lipton_m,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=lipton_m)
    add_crewratedtl_lipton_m.save()

    add_crewratedtl_mamee_m = CrewRateDtl(commissionitemclassguid=filter_mamee_m,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=mamee_m)
    add_crewratedtl_mamee_m.save()

    add_crewratedtl_mamypoko_m = CrewRateDtl(commissionitemclassguid=filter_mamypoko_m,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=mamypoko_m)
    add_crewratedtl_mamypoko_m.save()

    add_crewratedtl_dksh_m = CrewRateDtl(commissionitemclassguid=filter_dksh_m,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=dksh_m)
    add_crewratedtl_dksh_m.save()

    add_crewratedtl_sunquick_q = CrewRateDtl(commissionitemclassguid=filter_sunquick_q,crewrateguid=get_crewrateguid,crewtype=crew_type,commvalue=sunquick_q)
    add_crewratedtl_sunquick_q.save()