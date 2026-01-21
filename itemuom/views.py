from django.shortcuts import render

# Create your views here.
from .models import ItemUOM
from rest_framework import viewsets
from .serializers import ItemUOMSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ItemUOMViewSet(viewsets.ModelViewSet):
    queryset = ItemUOM.objects.all().order_by('uom')
    serializer_class = ItemUOMSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "uom": ["in", "exact"],
        'itemcode': ["in", "exact"],
    }
    search_fields = [
        "autokey",
        'itemcode',
        "uom"
    ]