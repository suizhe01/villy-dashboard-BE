from django.shortcuts import render

# Create your views here.
from .models import AcItemUOM
from rest_framework import viewsets
from .serializers import AcItemUOMSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class AcItemUOMViewSet(viewsets.ModelViewSet):
    queryset = AcItemUOM.objects.all().order_by('itemcode')
    serializer_class = AcItemUOMSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        # "companyautokey": ["in", "exact"], #icontains
        "uom": ["in", "exact"],
        'itemcode': ["in", "exact"],
        'udfispallet': ["in", "exact"],
    }
    search_fields = [
        "autokey",
        'itemcode',
        "uom",
        'udfispallet'
    ]