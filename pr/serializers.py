from .models import PR
from rest_framework import serializers

class PRSerializer(serializers.ModelSerializer):
    class Meta:
        model = PR
        fields = '__all__'
