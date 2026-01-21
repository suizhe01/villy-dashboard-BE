from .models import ItemBOM
from rest_framework import serializers

class ItemBOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBOM
        fields = '__all__'
