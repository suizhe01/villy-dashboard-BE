from .models import Creditor
from rest_framework import serializers

class CreditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creditor
        fields = '__all__'
