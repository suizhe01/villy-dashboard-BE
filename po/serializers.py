from .models import PO
from rest_framework import serializers

class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PO
        fields = '__all__'
