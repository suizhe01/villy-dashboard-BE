from .models import Lorry
from rest_framework import serializers

class LorrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lorry
        fields = '__all__'
