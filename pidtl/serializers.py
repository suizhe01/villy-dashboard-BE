from .models import PIDTL
from rest_framework import serializers

class PIDTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIDTL
        fields = '__all__'
