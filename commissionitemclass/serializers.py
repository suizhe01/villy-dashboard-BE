from .models import CommissionItemClass
from rest_framework import serializers

class CommissionItemClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionItemClass
        fields = '__all__'
