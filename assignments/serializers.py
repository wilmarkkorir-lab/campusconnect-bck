from rest_framework import serializers
from django.utils import timezone
from .models import Assignment, Submission


class AssignmentSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    is_past_deadline = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')

    def get_is_past_deadline(self, obj):
        return timezone.now() > obj.deadline


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('student', 'submitted_at', 'status')


class GradeSubmissionSerializer(serializers.Serializer):
    marks_obtained = serializers.DecimalField(max_digits=5, decimal_places=2)
    feedback = serializers.CharField(required=False, allow_blank=True)
