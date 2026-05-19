from crewrate.models import CrewRate
from crewratedtl.models import CrewRateDtl
from django.db import transaction
from _lib.panda import panda_uuid
from lorryplate.models import LorryPlate

def post_commission_template(employee_id,crew_name, crew_type,car_plate, sundry_m,dob_m,rb_q,yltc_q,le_q,cheers_q,rbpallet_q,sajioil_q,sajioilpallet_q,sajisweet_q,sajisweetpallet_q,lipton_m,mamee_m,mamypoko_m,dksh_m,sunquick_q,ecosafa_q,kara_m,kara_pallet_m,filter_sundry_m,filter_dob_m,filter_rb_q,filter_yltc_q,filter_le_q,filter_cheers_q,filter_rbpallet_q,filter_sajioil_q,filter_sajioilpallet_q,filter_sajisweet_q,filter_sajisweetpallet_q,filter_lipton_m,filter_mamee_m,filter_mamypoko_m,filter_dksh_m,filter_sunquick_q,filter_ecosafa_q,filter_kara_m,filter_kara_pallet_m):
    filter_lorry_plate = LorryPlate.objects.filter(lorrynumber=car_plate)
    if not filter_lorry_plate:
        new_lorry_plate = LorryPlate(lorrynumber=car_plate)
        new_lorry_plate.save()

    # Upsert CrewRate: update crewname if exists, create if not
    existing_crewrate = CrewRate.objects.filter(crewid=employee_id).first()
    if existing_crewrate:
        if existing_crewrate.crewname != crew_name:
            existing_crewrate.crewname = crew_name
            existing_crewrate.save()
        get_crewrateguid = existing_crewrate
    else:
        create_crewrate = CrewRate(crewid=employee_id,crewname=crew_name,isactive=1)
        create_crewrate.save()
        get_crewrateguid = CrewRate.objects.get(crewid=employee_id)

    # Upsert CrewRateDtl: update commvalue if exists, create if not
    commission_rates = [
        (filter_sundry_m, sundry_m),
        (filter_dob_m, dob_m),
        (filter_rb_q, rb_q),
        (filter_yltc_q, yltc_q),
        (filter_le_q, le_q),
        (filter_cheers_q, cheers_q),
        (filter_rbpallet_q, rbpallet_q),
        (filter_sajioil_q, sajioil_q),
        (filter_sajioilpallet_q, sajioilpallet_q),
        (filter_sajisweet_q, sajisweet_q),
        (filter_sajisweetpallet_q, sajisweetpallet_q),
        (filter_lipton_m, lipton_m),
        (filter_mamee_m, mamee_m),
        (filter_mamypoko_m, mamypoko_m),
        (filter_dksh_m, dksh_m),
        (filter_sunquick_q, sunquick_q),
        (filter_ecosafa_q, ecosafa_q),
        (filter_kara_m, kara_m),
        (filter_kara_pallet_m, kara_pallet_m),
    ]

    for filter_itemclass, comm_value in commission_rates:
        if filter_itemclass is not None:
            existing_dtl = CrewRateDtl.objects.filter(
                commissionitemclassguid=filter_itemclass,
                crewrateguid=get_crewrateguid,
                crewtype=crew_type
            ).first()

            if existing_dtl:
                if existing_dtl.commvalue != comm_value:
                    existing_dtl.commvalue = comm_value
                    existing_dtl.save()
            else:
                new_dtl = CrewRateDtl(
                    commissionitemclassguid=filter_itemclass,
                    crewrateguid=get_crewrateguid,
                    crewtype=crew_type,
                    commvalue=comm_value
                )
                new_dtl.save()