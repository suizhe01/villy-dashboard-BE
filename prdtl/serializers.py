from .models import PRDTL
from rest_framework import serializers

class PRDTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = PRDTL
        fields = '__all__'
