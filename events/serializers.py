from rest_framework import serializers
from .models import Event, EventRegistration


class EventRegistrationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = EventRegistration
        fields = '__all__'
        read_only_fields = ('user', 'qr_code', 'registered_at')


class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.full_name', read_only=True)
    attendee_count = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('organizer', 'created_at')

    def get_attendee_count(self, obj):
        return obj.registrations.filter(status='registered').count()

    def get_is_registered(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.registrations.filter(user=request.user).exists()
        return False
