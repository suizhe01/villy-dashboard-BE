from .models import ItemGroup
from rest_framework import serializers

class ItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemGroup
        fields = '__all__'
