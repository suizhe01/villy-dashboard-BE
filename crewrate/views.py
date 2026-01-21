from django.shortcuts import render

# Create your views here.
from .models import CrewRate
from rest_framework import viewsets
from .serializers import CrewRateSerializer
from rest_framework import filters

class CrewRateViewSet(viewsets.ModelViewSet):
    queryset = CrewRate.objects.all().order_by('crewrateguid')
    serializer_class = CrewRateSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "crewrateguid": ["in", "exact"],#icontains
    }
    search_fields = [
        "crewrateguid",
    ]