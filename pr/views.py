from django.shortcuts import render

# Create your views here.
from .models import PR
from rest_framework import viewsets
from .serializers import PRSerializer
from rest_framework import filters

class PRViewSet(viewsets.ModelViewSet):
    queryset = PR.objects.all().order_by('docno')
    serializer_class = PRSerializer
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