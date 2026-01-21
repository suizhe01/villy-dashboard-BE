from django.shortcuts import render

# Create your views here.
from .models import ItemClass
from rest_framework import viewsets
from .serializers import ItemClassSerializer
from rest_framework import filters

class ItemClassViewSet(viewsets.ModelViewSet):
    queryset = ItemClass.objects.all().order_by('itemclassguid')
    serializer_class = ItemClassSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "itemclassguid": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "itemclass": ["in", "exact"],
    }
    search_fields = [
        "itemclassguid",
        "debtortype",
        "itemclass"
    ]