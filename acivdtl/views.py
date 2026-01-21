from django.shortcuts import render

# Create your views here.
from .models import AcIVDTL
from rest_framework import viewsets
from .serializers import AcIVDTLSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class AcIVDTLViewSet(viewsets.ModelViewSet):
    queryset = AcIVDTL.objects.all().order_by('dockey')
    serializer_class = AcIVDTLSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = {
        "dockey": ["in", "exact"],
        "itemcode": ["in", "exact"],
        "location": ["in", "exact"],
    }
    search_fields = [
        "dockey",
    ]