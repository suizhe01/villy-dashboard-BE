from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from .models import AcTerms
from rest_framework import viewsets
from .serializers import AcTermsSerializer
from rest_framework import filters

class AcTermsViewSet(viewsets.ModelViewSet):
    queryset = AcTerms.objects.all().order_by('autokey')
    serializer_class = AcTermsSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "displayterm": ["in","exact"],
        "terms": ["in", "exact"],
        "lastupdate": ["in", "exact"],
        "termtype": ["in", "exact"],
        "termdays": ["in", "exact"],
        "discountdays": ["in", "exact"],
        "discountpercent": ["in", "exact"]
    }
    search_fields = [
        "autokey",
        "displayterm",
        "terms",
        "lastupdate",
        "termtype",
        "termdays",
        "discountdays",
        "discountpercent"
    ]