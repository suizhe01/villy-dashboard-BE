from .models import AcSalesAgent
from rest_framework import serializers

class AcSalesAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcSalesAgent
        fields = '__all__'
