from .models import ItemBatch
from rest_framework import serializers

class ItemBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBatch
        fields = '__all__'
