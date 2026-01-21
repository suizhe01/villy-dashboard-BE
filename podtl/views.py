from django.shortcuts import render

# Create your views here.
from .models import PODTL
from rest_framework import viewsets
from .serializers import PODTLSerializer
from rest_framework import filters

class PODTLViewSet(viewsets.ModelViewSet):
    queryset = PODTL.objects.all().order_by('autokey')
    serializer_class = PODTLSerializer
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