from .models import Crewdtl
from rest_framework import serializers

class CrewdtlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crewdtl
        fields = '__all__'
