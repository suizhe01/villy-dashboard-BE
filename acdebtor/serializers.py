from .models import AcDebtor
from rest_framework import serializers

class AcDebtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcDebtor
        fields = '__all__'
