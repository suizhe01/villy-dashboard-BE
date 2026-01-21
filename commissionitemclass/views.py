from django.shortcuts import render

# Create your views here.
from .models import CommissionItemClass
from rest_framework import viewsets
from .serializers import CommissionItemClassSerializer
from rest_framework import filters

class CommissionItemClassViewSet(viewsets.ModelViewSet):
    queryset = CommissionItemClass.objects.all().order_by('commissionitemclassguid')
    serializer_class = CommissionItemClassSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "commissionitemclassguid": ["in", "exact"],#icontains
    }
    search_fields = [
        "commissionitemclassguid",
    ]