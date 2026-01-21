from django.shortcuts import render

# Create your views here.
from .models import Lorry
from rest_framework import viewsets
from .serializers import LorrySerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class LorryViewSet(viewsets.ModelViewSet):
    queryset = Lorry.objects.all().order_by('lorryguid')
    serializer_class = LorrySerializer
    filter_backends = (
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "lorryguid": ["in", "exact"],#icontains
        "lorrynumber": ["in", "exact"],#icontains
        "docdate": ["lte", "gte"]
    }
    search_fields = [
        "lorryguid",
        "lorrynumber"
    ]