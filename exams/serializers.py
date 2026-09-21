from rest_framework import serializers
from .models import Exam, ExamResult


class ExamSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'


class ExamResultSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = ExamResult
        fields = '__all__'
        read_only_fields = ('student',)
