from django.contrib import admin

# Register your models here.
from .models import TaxType

admin.site.register(TaxType)