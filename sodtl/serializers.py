from .models import SODTL
from rest_framework import serializers

class SODTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = SODTL
        fields = '__all__'
