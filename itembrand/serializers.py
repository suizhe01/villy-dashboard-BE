from .models import ItemBrand
from rest_framework import serializers

class ItemBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBrand
        fields = '__all__'
