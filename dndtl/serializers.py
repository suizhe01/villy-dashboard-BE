from .models import DNDTL
from rest_framework import serializers

class DNDTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNDTL
        fields = '__all__'
