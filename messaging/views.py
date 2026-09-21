from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationListView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ConversationDetailView(generics.RetrieveAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation = generics.get_object_or_404(
            Conversation, id=self.kwargs['conversation_id'], participants=self.request.user
        )
        # Mark messages as read
        conversation.messages.exclude(sender=self.request.user).update(is_read=True)
        return conversation.messages.filter(is_deleted=False)

    def perform_create(self, serializer):
        conversation = generics.get_object_or_404(
            Conversation, id=self.kwargs['conversation_id'], participants=self.request.user
        )
        serializer.save(sender=self.request.user, conversation=conversation)


class DeleteMessageView(APIView):
    def delete(self, request, message_id):
        message = generics.get_object_or_404(Message, id=message_id, sender=request.user)
        message.is_deleted = True
        message.content = 'This message was deleted.'
        message.save()
        return Response({'message': 'Message deleted.'})


class DirectMessageView(APIView):
    """Start or get a direct conversation with another user."""
    def post(self, request):
        other_user_id = request.data.get('user_id')
        from accounts.models import User
        other_user = generics.get_object_or_404(User, id=other_user_id)
        # Find existing direct conversation
        existing = Conversation.objects.filter(
            conversation_type='direct', participants=request.user
        ).filter(participants=other_user)
        if existing.exists():
            return Response(ConversationSerializer(existing.first(), context={'request': request}).data)
        conversation = Conversation.objects.create(
            conversation_type='direct', created_by=request.user
        )
        conversation.participants.add(request.user, other_user)
        return Response(
            ConversationSerializer(conversation, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
