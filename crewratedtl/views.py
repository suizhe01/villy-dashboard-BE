from django.shortcuts import render

# Create your views here.
from .models import CrewRateDtl
from rest_framework import viewsets
from .serializers import CrewRateDtlSerializer
from rest_framework import filters

class CrewRateDtlViewSet(viewsets.ModelViewSet):
    queryset = CrewRateDtl.objects.all().order_by('crewratedtlguid')
    serializer_class = CrewRateDtlSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "crewratedtlguid": ["in", "exact"],#icontains
    }
    search_fields = [
        "crewratedtlguid",
    ]