from .models import ItemCategory
from rest_framework import serializers

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = '__all__'
