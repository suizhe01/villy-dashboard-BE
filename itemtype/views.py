from django.shortcuts import render

# Create your views here.
from .models import ItemType
from rest_framework import viewsets
from .serializers import ItemTypeSerializer
from rest_framework import filters

class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all().order_by('itemtype')
    serializer_class = ItemTypeSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "itemtype": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "itemtype",
        'companyautokey'
    ]