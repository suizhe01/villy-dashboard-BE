from .models import CN
from rest_framework import serializers

class CNSerializer(serializers.ModelSerializer):
    class Meta:
        model = CN
        fields = '__all__'
