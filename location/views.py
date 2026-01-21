from django.shortcuts import render

# Create your views here.
from .models import Location
from rest_framework import viewsets
from .serializers import LocationSerializer
from rest_framework import filters

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('location')
    serializer_class = LocationSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "location": ['in','exact','icontains']
    }
    search_fields = [
        "autokey",
        'companyautokey',
        'location'
    ]