from .models import GRDTL
from rest_framework import serializers

class GRDTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = GRDTL
        fields = '__all__'
