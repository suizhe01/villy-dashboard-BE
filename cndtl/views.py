from django.shortcuts import render

# Create your views here.
from .models import CNDTL
from rest_framework import viewsets
from .serializers import CNDTLSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class CNDTLViewSet(viewsets.ModelViewSet):
    queryset = CNDTL.objects.all().order_by('autokey')
    serializer_class = CNDTLSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        "autokey": ["in", "exact"],#icontains
        "headerautokey": ["in", "exact"],
        "itemcode": ["in", "exact"],
        "location": ["in", "exact"],
    }
    search_fields = [
        "autokey",
    ]