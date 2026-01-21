from .models import Crew
from rest_framework import serializers

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'
