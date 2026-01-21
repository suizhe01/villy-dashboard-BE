from django.shortcuts import render

# Create your views here.
from .models import ADJ
from rest_framework import viewsets
from .serializers import ADJSerializer
from rest_framework import filters

class ADJViewSet(viewsets.ModelViewSet):
    queryset = ADJ.objects.all().order_by('docno')
    serializer_class = ADJSerializer
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