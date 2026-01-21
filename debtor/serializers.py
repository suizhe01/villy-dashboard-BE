from .models import Debtor
from rest_framework import serializers

class DebtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debtor
        fields = '__all__'
