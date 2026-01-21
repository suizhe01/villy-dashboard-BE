from .models import AcTerms
from rest_framework import serializers

class AcTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcTerms
        fields = '__all__'
