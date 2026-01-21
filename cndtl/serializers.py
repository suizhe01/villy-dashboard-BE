from .models import CNDTL
from rest_framework import serializers

class CNDTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CNDTL
        fields = '__all__'
