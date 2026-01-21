from .models import DebtorType
from rest_framework import serializers

class DebtorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtorType
        fields = '__all__'
