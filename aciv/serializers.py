from .models import AcIV
from rest_framework import serializers

class AcIVSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcIV
        fields = '__all__'
