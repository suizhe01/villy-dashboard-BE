from django.shortcuts import render

# Create your views here.
from .models import Company
from rest_framework import viewsets
from .serializers import CompanySerializer
from rest_framework import filters

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('code')
    serializer_class = CompanySerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "code": ["in", "exact"],
        "address": ["in", "exact"],
        "registrationnum": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "code",
        "address",
        "registrationnum",
    ]