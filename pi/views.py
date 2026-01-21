from django.shortcuts import render

# Create your views here.
from .models import PI
from rest_framework import viewsets
from .serializers import PISerializer
from rest_framework import filters

class PIViewSet(viewsets.ModelViewSet):
    queryset = PI.objects.all().order_by('docno')
    serializer_class = PISerializer
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
        "debtortype",
        "docno"
    ]