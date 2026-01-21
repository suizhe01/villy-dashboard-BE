from .models import AcItem
from rest_framework import serializers

class AcItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcItem
        fields = '__all__'
