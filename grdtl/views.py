from django.shortcuts import render

# Create your views here.
from .models import GRDTL
from rest_framework import viewsets
from .serializers import GRDTLSerializer
from rest_framework import filters

class GRDTLViewSet(viewsets.ModelViewSet):
    queryset = GRDTL.objects.all().order_by('autokey')
    serializer_class = GRDTLSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],#icontains
    }
    search_fields = [
        "autokey","branchautokey"
    ]