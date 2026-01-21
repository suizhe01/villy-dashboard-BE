from django.shortcuts import render

# Create your views here.
from .models import SODTL
from rest_framework import viewsets
from .serializers import SODTLSerializer
from rest_framework import filters

class SODTLViewSet(viewsets.ModelViewSet):
    queryset = SODTL.objects.all().order_by('autokey')
    serializer_class = SODTLSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],#icontains
    }
    search_fields = [
        "autokey",
    ]