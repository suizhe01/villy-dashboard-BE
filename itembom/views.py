from django.shortcuts import render

# Create your views here.
from .models import ItemBOM
from rest_framework import viewsets
from .serializers import ItemBOMSerializer
from rest_framework import filters

class ItemBOMViewSet(viewsets.ModelViewSet):
    queryset = ItemBOM.objects.all().order_by('itemcode')
    serializer_class = ItemBOMSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "itemcode": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "debtortype",
        "itemcode"
    ]