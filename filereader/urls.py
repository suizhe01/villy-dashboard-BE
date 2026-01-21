# excelreader/urls.py
from django.urls import path
from .views import upload_and_process_excel

urlpatterns = [
    path('upload-and-process-excel/', upload_and_process_excel, name='upload_and_process_excel'),
]
