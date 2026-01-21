from django.shortcuts import render

# Create your views here.
from .models import DN
from rest_framework import viewsets
from .serializers import DNSerializer
from rest_framework import filters

class DNViewSet(viewsets.ModelViewSet):
    queryset = DN.objects.all().order_by('docno')
    serializer_class = DNSerializer
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