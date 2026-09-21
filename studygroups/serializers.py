from rest_framework import serializers
from .models import StudyGroup, StudyGroupMember, StudySession, StudyGroupResource


class StudyGroupMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = StudyGroupMember
        fields = '__all__'
        read_only_fields = ('user', 'joined_at')


class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')


class StudyGroupResourceSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)

    class Meta:
        model = StudyGroupResource
        fields = '__all__'
        read_only_fields = ('uploaded_by', 'created_at')


class StudyGroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = StudyGroup
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')

    def get_member_count(self, obj):
        return obj.studygroupmember_set.count()

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.studygroupmember_set.filter(user=request.user).exists()
        return False
