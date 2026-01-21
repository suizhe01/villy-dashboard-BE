from .models import ADJ
from rest_framework import serializers

class ADJSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADJ
        fields = '__all__'
