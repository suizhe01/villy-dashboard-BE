from django.shortcuts import render

# Create your views here.
from .models import Branch
from rest_framework import viewsets
from .serializers import BranchSerializer
from rest_framework import filters

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('code')
    serializer_class = BranchSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "code": ["in", "exact"],
        "address": ["in", "exact","icontains"],
        "registorno": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "code",
        "address",
        "registorno",
        'companyautokey'
    ]