from .models import CreditorType
from rest_framework import serializers

class CreditorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditorType
        fields = '__all__'
