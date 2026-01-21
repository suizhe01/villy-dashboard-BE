from datetime import datetime
from django.utils import timezone

def panda_uuid():
    import uuid
    return str(uuid.uuid4().hex).upper()

def convert_date_from_dd_mm_yyyy(date_str):
    date_object = datetime.strptime(date_str, "%d/%m/%Y")
    # Convert the date to the desired format
    converted_date = date_object.strftime('%Y-%m-%d')
    return converted_date

def current_date_time():
    return timezone.now()
