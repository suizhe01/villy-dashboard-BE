from django.shortcuts import render

# Create your views here.
from .models import Crewdtl
from rest_framework import viewsets
from .serializers import CrewdtlSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class CrewdtlViewSet(viewsets.ModelViewSet):
    queryset = Crewdtl.objects.all().order_by('crewdtlguid')
    serializer_class = CrewdtlSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "crewdtlguid": ["in", "exact"],#icontains
    }
    search_fields = [
        "crewdtlguid",
    ]