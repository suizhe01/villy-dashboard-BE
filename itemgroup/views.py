from django.shortcuts import render

# Create your views here.
from .models import ItemGroup
from rest_framework import viewsets
from .serializers import ItemGroupSerializer
from rest_framework import filters

class ItemGroupViewSet(viewsets.ModelViewSet):
    queryset = ItemGroup.objects.all().order_by('autokey')
    serializer_class = ItemGroupSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
       
    }
    search_fields = [
        "autokey",
        "debtortype",
    ]