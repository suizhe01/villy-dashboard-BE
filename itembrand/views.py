from django.shortcuts import render

# Create your views here.
from .models import ItemBrand
from rest_framework import viewsets
from .serializers import ItemBrandSerializer
from rest_framework import filters

class ItemBrandViewSet(viewsets.ModelViewSet):
    queryset = ItemBrand.objects.all().order_by('itembrand')
    serializer_class = ItemBrandSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "itembrand": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "debtortype",
        "itembrand"
    ]