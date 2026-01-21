from .models import AcItemUOM
from rest_framework import serializers

class AcItemUOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcItemUOM
        fields = '__all__'
