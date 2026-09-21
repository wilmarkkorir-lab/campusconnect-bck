from rest_framework import serializers
from .models import Portfolio, Project, Certificate, Achievement, WorkExperience, Leadership
import secrets


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('portfolio', 'created_at')


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'
        read_only_fields = ('portfolio', 'created_at')


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
        read_only_fields = ('portfolio', 'created_at')


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
        read_only_fields = ('portfolio', 'created_at')


class LeadershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leadership
        fields = '__all__'
        read_only_fields = ('portfolio', 'created_at')


class PortfolioSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)
    leadership_roles = LeadershipSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Portfolio
        fields = '__all__'
        read_only_fields = ('user', 'share_token', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['share_token'] = secrets.token_urlsafe(32)
        return super().create(validated_data)
