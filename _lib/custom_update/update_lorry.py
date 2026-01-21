from lorry.models import Lorry


def update_lorry_number(lorry_guid, lorry_number, date):
    if lorry_number and date:
        updated_count = Lorry.objects.filter(lorryguid=lorry_guid).update(lorrynumber=lorry_number, docdate=date)    
    elif lorry_number:
        updated_count = Lorry.objects.filter(lorryguid=lorry_guid).update(lorrynumber=lorry_number)    
    elif date:
        updated_count = Lorry.objects.filter(lorryguid=lorry_guid).update(docdate=date)    

    
    if updated_count == 0:
        return 'error: lorry not found'
    return 'succes'