from .models import ItemPrice
from rest_framework import serializers

class ItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPrice
        fields = '__all__'
