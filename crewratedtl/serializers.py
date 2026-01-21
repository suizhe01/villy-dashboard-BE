from .models import CrewRateDtl
from rest_framework import serializers

class CrewRateDtlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewRateDtl
        fields = '__all__'
