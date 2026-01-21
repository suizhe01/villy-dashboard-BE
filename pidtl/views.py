from django.shortcuts import render

# Create your views here.
from .models import PIDTL
from rest_framework import viewsets
from .serializers import PIDTLSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class PIDTLViewSet(viewsets.ModelViewSet):
    queryset = PIDTL.objects.all().order_by('autokey')
    serializer_class = PIDTLSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        "autokey": ["in", "exact"], #icontains
        "headerautokey": ["in", "exact"], #icontains
        "itemcode": ["in", "exact"], #icontains
        "location": ["in", "exact"], #icontains
    }
    search_fields = [
        "autokey","branchautokey"
    ]