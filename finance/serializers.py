from rest_framework import serializers
from .models import FeeStructure


class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
