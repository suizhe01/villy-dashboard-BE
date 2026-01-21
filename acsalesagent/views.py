from django.shortcuts import render

# Create your views here.
from .models import AcSalesAgent
from rest_framework import viewsets
from .serializers import AcSalesAgentSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class AcSalesAgentViewSet(viewsets.ModelViewSet):
    queryset = AcSalesAgent.objects.all().order_by('salesagent')
    serializer_class = AcSalesAgentSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        "autokey": ["in", "exact"],#icontains
        "salesagent": ["in", "exact"],
        # "docno": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "salesagent"
    ]