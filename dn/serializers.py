from .models import DN
from rest_framework import serializers

class DNSerializer(serializers.ModelSerializer):
    class Meta:
        model = DN
        fields = '__all__'
