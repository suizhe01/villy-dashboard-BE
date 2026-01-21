from django.shortcuts import render

# Create your views here.
from .models import AcItem
from rest_framework import viewsets
from .serializers import AcItemSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class AcItemViewSet(viewsets.ModelViewSet):
    queryset = AcItem.objects.all().order_by('itemcode')
    serializer_class = AcItemSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        # "companyautokey": ["in", "exact"], #icontains
        "itemcode": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "debtortype",
        "itemcode"
    ]