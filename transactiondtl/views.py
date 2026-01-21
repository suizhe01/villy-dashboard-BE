from django.shortcuts import render

# Create your views here.
from .models import TransactionDtl
from rest_framework import viewsets
from .serializers import TransactionDtlSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class TransactionDtlViewSet(viewsets.ModelViewSet):
    queryset = TransactionDtl.objects.all().order_by('transactiondtlguid')
    serializer_class = TransactionDtlSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "transactiondtlguid": ["in", "exact"],#icontains
    }
    search_fields = [
        "transactiondtlguid",
    ]