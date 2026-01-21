from .models import IVDTL
from rest_framework import serializers

class IVDTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = IVDTL
        fields = '__all__'
