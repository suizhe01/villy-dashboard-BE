from .models import CrewRate
from rest_framework import serializers

class CrewRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewRate
        fields = '__all__'
