from .models import SalesAgent
from rest_framework import serializers

class SalesAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesAgent
        fields = '__all__'
