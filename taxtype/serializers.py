from .models import TaxType
from rest_framework import serializers

class TaxTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxType
        fields = '__all__'
