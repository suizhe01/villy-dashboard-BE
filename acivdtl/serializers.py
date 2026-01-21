from .models import AcIVDTL
from rest_framework import serializers

class AcIVDTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcIVDTL
        fields = '__all__'
