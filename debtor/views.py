from django.shortcuts import render

# Create your views here.
from .models import Debtor
from rest_framework import viewsets
from .serializers import DebtorSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny

class DebtorViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Debtor.objects.all().order_by('companyautokey')
    serializer_class = DebtorSerializer
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