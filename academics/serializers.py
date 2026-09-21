from rest_framework import serializers
from .models import Course, Enrollment, Material, MaterialCategory, MaterialBookmark, Timetable, AcademicCalendar, PersonalReminder


class CourseSerializer(serializers.ModelSerializer):
    lecturer_name = serializers.CharField(source='lecturer.full_name', read_only=True)
    enrolled_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_enrolled_count(self, obj):
        return obj.enrollments.filter(is_active=True).count()


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = Enrollment
        fields = ('id', 'course', 'course_id', 'enrolled_at', 'is_active')
        read_only_fields = ('enrolled_at',)


class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = '__all__'
        read_only_fields = ('uploaded_by', 'download_count', 'created_at')

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return MaterialBookmark.objects.filter(user=request.user, material=obj).exists()
        return False


class TimetableSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = Timetable
        fields = '__all__'


class AcademicCalendarSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = AcademicCalendar
        fields = '__all__'
        read_only_fields = ('created_by',)


class PersonalReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalReminder
        fields = '__all__'
        read_only_fields = ('user',)
