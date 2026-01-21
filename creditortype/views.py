from django.shortcuts import render

# Create your views here.
from .models import CreditorType
from rest_framework import viewsets
from .serializers import CreditorTypeSerializer
from rest_framework import filters

class CreditorTypeViewSet(viewsets.ModelViewSet):
    queryset = CreditorType.objects.all().order_by('creditortype')
    serializer_class = CreditorTypeSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "creditortype": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "creditortype",
        'companyautokey'
    ]