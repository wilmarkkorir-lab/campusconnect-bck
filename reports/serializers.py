from rest_framework import serializers
from .models import Report, ModerationLog


class ReportSerializer(serializers.ModelSerializer):
    reported_by_name = serializers.CharField(source='reported_by.full_name', read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('reported_by', 'status', 'reviewed_by', 'action_taken', 'admin_notes', 'created_at', 'updated_at')


class ModerationLogSerializer(serializers.ModelSerializer):
    moderator_name = serializers.CharField(source='moderator.full_name', read_only=True)

    class Meta:
        model = ModerationLog
        fields = '__all__'
        read_only_fields = ('moderator', 'created_at')


class ReportAdminSerializer(serializers.ModelSerializer):
    moderation_logs = ModerationLogSerializer(many=True, read_only=True)
    reported_by_name = serializers.CharField(source='reported_by.full_name', read_only=True)
    reported_user_name = serializers.CharField(source='reported_user.full_name', read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('reported_by', 'created_at')
