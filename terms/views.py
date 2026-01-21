from django.shortcuts import render

# Create your views here.
from .models import Terms
from rest_framework import viewsets
from .serializers import TermsSerializer
from rest_framework import filters

class TermsViewSet(viewsets.ModelViewSet):
    queryset = Terms.objects.all().order_by('autokey')
    serializer_class = TermsSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = {
        "autokey": ["in", "exact"],
        "companyautokey": ["in", "exact"], #icontains
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
        "companyautokey",
        "displayterm",
        "terms",
        "lastupdate",
        "termtype",
        "termdays",
        "discountdays",
        "discountpercent"
    ]