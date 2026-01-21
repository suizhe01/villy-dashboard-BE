from .models import SO
from rest_framework import serializers

class SOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SO
        fields = '__all__'
