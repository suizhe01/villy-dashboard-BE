from django.shortcuts import render

# Create your views here.
from .models import PO
from rest_framework import viewsets
from .serializers import POSerializer
from rest_framework import filters

class POViewSet(viewsets.ModelViewSet):
    queryset = PO.objects.all().order_by('docno')
    serializer_class = POSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],#icontains
        "docno": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "docno"
    ]