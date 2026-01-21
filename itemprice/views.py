from django.shortcuts import render

# Create your views here.
from .models import ItemPrice
from rest_framework import viewsets
from .serializers import ItemPriceSerializer
from rest_framework import filters

class ItemPriceViewSet(viewsets.ModelViewSet):
    queryset = ItemPrice.objects.all().order_by('pricecategory')
    serializer_class = ItemPriceSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "pricecategory": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "debtortype",
        "pricecategory"
    ]