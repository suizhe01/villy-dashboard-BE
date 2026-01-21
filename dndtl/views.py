from django.shortcuts import render

# Create your views here.
from .models import DNDTL
from rest_framework import viewsets
from .serializers import DNDTLSerializer
from rest_framework import filters

class DNDTLViewSet(viewsets.ModelViewSet):
    queryset = DNDTL.objects.all().order_by('autokey')
    serializer_class = DNDTLSerializer
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