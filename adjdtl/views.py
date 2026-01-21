from django.shortcuts import render

# Create your views here.
from .models import ADJDTL
from rest_framework import viewsets
from .serializers import ADJDTLSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ADJDTLViewSet(viewsets.ModelViewSet):
    queryset = ADJDTL.objects.all().order_by('autokey')
    serializer_class = ADJDTLSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],#icontains
    }
    search_fields = [
        "autokey",
    ]