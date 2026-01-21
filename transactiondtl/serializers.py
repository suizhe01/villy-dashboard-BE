from .models import TransactionDtl
from rest_framework import serializers

class TransactionDtlSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDtl
        fields = '__all__'
