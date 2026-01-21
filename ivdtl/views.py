from django.shortcuts import render

# Create your views here.
from .models import IVDTL
from rest_framework import viewsets
from .serializers import IVDTLSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class IVDTLViewSet(viewsets.ModelViewSet):
    queryset = IVDTL.objects.all().order_by('autokey')
    serializer_class = IVDTLSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        "headerautokey": ["in", "exact"],
        "autokey": ["in", "exact"],
        "itemcode": ["in", "exact"],
        "location": ["in", "exact"],
    }
    search_fields = [
        "autokey",
    ]