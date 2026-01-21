from .models import ItemUOM
from rest_framework import serializers

class ItemUOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemUOM
        fields = '__all__'
