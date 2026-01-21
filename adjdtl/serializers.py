from .models import ADJDTL
from rest_framework import serializers

class ADJDTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADJDTL
        fields = '__all__'
