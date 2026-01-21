from django.shortcuts import render

# Create your views here.
from .models import Item
from rest_framework import viewsets
from .serializers import ItemSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('itemcode')
    serializer_class = ItemSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
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