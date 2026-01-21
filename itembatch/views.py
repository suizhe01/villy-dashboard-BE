from django.shortcuts import render

# Create your views here.
from .models import ItemBatch
from rest_framework import viewsets
from .serializers import ItemBatchSerializer
from rest_framework import filters

class ItemBatchViewSet(viewsets.ModelViewSet):
    queryset = ItemBatch.objects.all().order_by('batchno')
    serializer_class = ItemBatchSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "batchno": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "debtortype",
        "batchno"
    ]