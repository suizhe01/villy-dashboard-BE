from django.shortcuts import render

# Create your views here.
from .models import LorryPlate
from rest_framework import viewsets
from .serializers import LorryPlateSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class LorryPlateViewSet(viewsets.ModelViewSet):
    queryset = LorryPlate.objects.all().order_by('lorryplateguid')
    serializer_class = LorryPlateSerializer
    filter_backends = (
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "lorryplateguid": ["in", "exact"],#icontains
        "lorrynumber": ["in", "exact"],#icontains
    }
    search_fields = [
        "lorryplateguid",
        "lorrynumber"
    ]