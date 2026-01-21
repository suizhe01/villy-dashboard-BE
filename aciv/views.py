from django.shortcuts import render

# Create your views here.
from .models import AcIV
from rest_framework import viewsets
from .serializers import AcIVSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class AcIVViewSet(viewsets.ModelViewSet):
    queryset = AcIV.objects.all().order_by('docno')
    serializer_class = AcIVSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        # "autokey": ["in", "exact"],#icontains
        # "branchautokey": ["in", "exact"],
        "docno": ["in", "exact"],
    }
    search_fields = [
        # "autokey",
        "docno"
    ]