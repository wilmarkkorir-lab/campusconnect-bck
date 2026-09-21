from rest_framework import serializers
from .models import Job, JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.full_name', read_only=True)

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('applicant', 'applied_at', 'status')


class JobSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source='posted_by.full_name', read_only=True)
    has_applied = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('posted_by', 'created_at')

    def get_has_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.applications.filter(applicant=request.user).exists()
        return False
