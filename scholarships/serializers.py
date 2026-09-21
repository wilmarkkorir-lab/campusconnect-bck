from rest_framework import serializers
from .models import Scholarship, SavedScholarship, ScholarshipApplication


class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipApplication
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class ScholarshipSerializer(serializers.ModelSerializer):
    is_saved = serializers.SerializerMethodField()
    application_status = serializers.SerializerMethodField()

    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ('posted_by', 'created_at')

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saves.filter(user=request.user).exists()
        return False

    def get_application_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            app = obj.applications.filter(user=request.user).first()
            return app.status if app else None
        return None
