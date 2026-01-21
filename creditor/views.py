from django.shortcuts import render

# Create your views here.
from .models import Creditor
from rest_framework import viewsets
from .serializers import CreditorSerializer
from rest_framework import filters

class CreditorViewSet(viewsets.ModelViewSet):
    queryset = Creditor.objects.all().order_by('companyautokey')
    serializer_class = CreditorSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "registorno": ["in", "exact"],
        "companyname": ["in", "exact"],
        "accno": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "registorno",
        'companyautokey',
        "companyname",
        "accno",
    ]