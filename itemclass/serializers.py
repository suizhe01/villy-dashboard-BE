from .models import ItemClass
from rest_framework import serializers

class ItemClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemClass
        fields = '__all__'
