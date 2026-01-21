from django.shortcuts import render

# Create your views here.
from .models import ItemCategory
from rest_framework import viewsets
from .serializers import ItemCategorySerializer
from rest_framework import filters

class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all().order_by('itemcategory')
    serializer_class = ItemCategorySerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "itemcategory": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "debtortype",
        "itemcategory"
    ]