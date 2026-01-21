from .models import PI
from rest_framework import serializers

class PISerializer(serializers.ModelSerializer):
    class Meta:
        model = PI
        fields = '__all__'
