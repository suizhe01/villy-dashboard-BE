from django.shortcuts import render

# Create your views here.
from .models import DebtorType
from rest_framework import viewsets
from .serializers import DebtorTypeSerializer
from rest_framework import filters

class DebtorTypeViewSet(viewsets.ModelViewSet):
    queryset = DebtorType.objects.all().order_by('debtortype')
    serializer_class = DebtorTypeSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "debtortype": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "debtortype",
        'companyautokey'
    ]