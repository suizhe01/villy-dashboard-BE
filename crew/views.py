from django.shortcuts import render

# Create your views here.
from .models import Crew
from rest_framework import viewsets
from .serializers import CrewSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all().order_by('crewguid')
    serializer_class = CrewSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "crewguid": ["in", "exact"],#icontains
    }
    search_fields = [
        "crewguid",
    ]