from django.shortcuts import render

# Create your views here.
from .models import CN
from rest_framework import viewsets
from .serializers import CNSerializer
from rest_framework import filters

class CNViewSet(viewsets.ModelViewSet):
    queryset = CN.objects.all().order_by('docno')
    serializer_class = CNSerializer
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