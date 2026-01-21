from .models import IV
from rest_framework import serializers

class IVSerializer(serializers.ModelSerializer):
    class Meta:
        model = IV
        fields = '__all__'
