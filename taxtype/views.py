from django.shortcuts import render

# Create your views here.
from .models import TaxType
from rest_framework import viewsets
from .serializers import TaxTypeSerializer
from rest_framework import filters

class TaxTypeViewSet(viewsets.ModelViewSet):
    queryset = TaxType.objects.all().order_by('taxaccno')
    serializer_class = TaxTypeSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "taxtype": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "taxtype",
        'companyautokey'
    ]