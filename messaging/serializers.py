from rest_framework import serializers
from .models import Conversation, Message, MessageReadStatus
from accounts.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'created_at')


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, source='participants',
        queryset=__import__('accounts.models', fromlist=['User']).User.objects.all()
    )
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def get_last_message(self, obj):
        msg = obj.messages.filter(is_deleted=False).last()
        if msg:
            return MessageSerializer(msg).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        if self.context['request'].user not in participants:
            conversation.participants.add(self.context['request'].user)
        return conversation
