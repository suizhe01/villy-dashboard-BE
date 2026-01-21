from .models import LorryPlate
from rest_framework import serializers

class LorryPlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LorryPlate
        fields = '__all__'
