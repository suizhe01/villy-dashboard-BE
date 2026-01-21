from django.shortcuts import render

# Create your views here.
from .models import PRDTL
from rest_framework import viewsets
from .serializers import PRDTLSerializer
from rest_framework import filters

class PRDTLViewSet(viewsets.ModelViewSet):
    queryset = PRDTL.objects.all().order_by('autokey')
    serializer_class = PRDTLSerializer
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