from django.shortcuts import render

# Create your views here.
from .models import AcDebtor
from rest_framework import viewsets
from .serializers import AcDebtorSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny

class AcDebtorViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = AcDebtor.objects.all().order_by('accno')
    serializer_class = AcDebtorSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "registorno": ["in", "exact"],
        "companyname": ["in", "exact"],
        "accno": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "registorno",
        "companyname",
        "accno",
    ]