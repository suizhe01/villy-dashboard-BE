from django.shortcuts import render

# Create your views here.
from .models import GR
from rest_framework import viewsets
from .serializers import GRSerializer
from rest_framework import filters

class GRViewSet(viewsets.ModelViewSet):
    queryset = GR.objects.all().order_by('docno')
    serializer_class = GRSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
        "docno": ["in", "exact"],
    }
    search_fields = [
        "autokey",
        "docno"
    ]