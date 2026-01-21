from .models import PODTL
from rest_framework import serializers

class PODTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = PODTL
        fields = '__all__'
