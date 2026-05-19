import pandas as pd
from django.http import JsonResponse
from rest_framework import status

def process_commission_file(dataframe):
    commission = {'commission': []}
    dataframe = pd.read_excel(dataframe, dtype={'CODE': str})

    # store_itemcode = []
    # item_uom_dict = {(item.itemcode.itemcode, item.uom): item for item in ItemUOM.objects.select_related('itemcode').all()}

    with pd.option_context('display.max_row', None):
        selected_columns = dataframe[['CODE','NAME','DRIVER','CARPLATE','SUNDRY($)','DOB($)','RB(Q)','YLTC(Q)','LE(Q)','CHEERS(Q)','RBPALLET(Q)','SAJIOIL(Q)','SAJIOILPALLET(Q)','SAJISWEET(Q)','SAJISWEETPALLET(Q)','LIPTON($)','MAMEE($)','MAMYPOKO($)','DKSH($)','SUNQUICK(Q)','ECOSAFA(Q)','KARA($)','KARAPALLET($)']]

        for index, row in selected_columns.iterrows():
            raw_code = row['CODE']
            if pd.isna(raw_code) or str(raw_code).strip() == '':
                continue
            employee_id = str(raw_code).zfill(4)
            crew_name = row['NAME']
            driver = row['DRIVER']
            car_plate = row['CARPLATE']
            sundry_m = row['SUNDRY($)']
            dob_m = row['DOB($)']
            rb_q = row['RB(Q)']
            yltc_q = row['YLTC(Q)']
            le_q = row['LE(Q)']
            cheers_q = row['CHEERS(Q)']
            rb_pallet_q = row['RBPALLET(Q)']
            sajioil_q = row['SAJIOIL(Q)']
            sajioil_pallet_q = row['SAJIOILPALLET(Q)']
            sajisweet_q = row['SAJISWEET(Q)']
            sajisweet_pallet_q = row['SAJISWEETPALLET(Q)']
            lipton_m = row['LIPTON($)']
            mamee_m = row['MAMEE($)']
            mamypoko_m = row['MAMYPOKO($)']
            sunquick_q = row['SUNQUICK(Q)']
            dksh_m = row['DKSH($)']
            ecosafa_q = row['ECOSAFA(Q)']
            kara_m = row['KARA($)']
            kara_pallet_m = row['KARAPALLET($)']

            if pd.isna(car_plate):
                car_plate = ""


            if driver == 1:
                crew_type = 'Driver'
            else:
                crew_type = 'Assistant'

            commission['commission'].append({
                    'employee_id': employee_id,
                    'crew_name': crew_name,
                    'crew_type': crew_type,
                    'car_plate': car_plate,
                    'SUNDRY($)': sundry_m,
                    'DOB($)': dob_m,
                    'LIPTON($)': lipton_m,
                    'MAMEE($)': mamee_m,
                    'MAMYPOKO($)': mamypoko_m,
                    'DKSH($)': dksh_m,
                    'RB(Q)': rb_q,
                    'YLTC(Q)': yltc_q,
                    'LE(Q)': le_q,
                    'CHEERS(Q)': cheers_q,
                    'RBPALLET(Q)': rb_pallet_q,
                    'SAJIOIL(Q)': sajioil_q,
                    'SAJIOILPALLET(Q)': sajioil_pallet_q,
                    'SAJISWEET(Q)': sajisweet_q,
                    'SAJISWEETPALLET(Q)': sajisweet_pallet_q,
                    'SUNQUICK(Q)': sunquick_q,
                    'ECOSAFA(Q)': ecosafa_q,
                    'KARA($)': kara_m,
                    'KARAPALLET($)': kara_pallet_m
                })
                

            

    return JsonResponse(commission, safe=False, status=status.HTTP_200_OK)