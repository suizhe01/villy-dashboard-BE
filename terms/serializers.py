from .models import Terms
from rest_framework import serializers

class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'
