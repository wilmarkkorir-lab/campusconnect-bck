from rest_framework import serializers
from .models import University, Campus, Faculty, Department, Program, CampusLocation


class CampusLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusLocation
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    programs = ProgramSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = '__all__'


class CampusSerializer(serializers.ModelSerializer):
    locations = CampusLocationSerializer(many=True, read_only=True)

    class Meta:
        model = Campus
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    campuses = CampusSerializer(many=True, read_only=True)
    faculties = FacultySerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = '__all__'


class UniversityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('id', 'name', 'short_name', 'logo', 'website')
