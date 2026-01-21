from django.shortcuts import render

# Create your views here.
from .models import Transaction
from rest_framework import viewsets
from .serializers import TransactionSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('transactionguid')
    serializer_class = TransactionSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "transactionguid": ["in", "exact"],#icontains
    }
    search_fields = [
        "transactionguid",
    ]