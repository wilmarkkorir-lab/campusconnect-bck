from rest_framework import serializers
from .models import EmergencyContact, EmergencyAnnouncement, IncidentReport


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'


class EmergencyAnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = EmergencyAnnouncement
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')


class IncidentReportSerializer(serializers.ModelSerializer):
    reported_by_name = serializers.CharField(source='reported_by.full_name', read_only=True)

    class Meta:
        model = IncidentReport
        fields = '__all__'
        read_only_fields = ('reported_by', 'status', 'created_at')
