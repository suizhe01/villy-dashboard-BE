from django.shortcuts import render

# Create your views here.
from .models import SO
from rest_framework import viewsets
from .serializers import SOSerializer
from rest_framework import filters

class SOViewSet(viewsets.ModelViewSet):
    queryset = SO.objects.all().order_by('docno')
    serializer_class = SOSerializer
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