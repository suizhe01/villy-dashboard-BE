from .models import GR
from rest_framework import serializers

class GRSerializer(serializers.ModelSerializer):
    class Meta:
        model = GR
        fields = '__all__'
