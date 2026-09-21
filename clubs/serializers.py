from rest_framework import serializers
from .models import Club, ClubMember, ClubAnnouncement


class ClubMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = ClubMember
        fields = '__all__'
        read_only_fields = ('user', 'joined_at')


class ClubAnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = ClubAnnouncement
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')


class ClubSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')

    def get_member_count(self, obj):
        return obj.memberships.count()

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.memberships.filter(user=request.user).exists()
        return False
