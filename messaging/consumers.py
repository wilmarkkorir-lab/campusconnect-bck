import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return
        if not await self.is_participant(user, self.conversation_id):
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'message')
        if message_type == 'message':
            content = data.get('content', '')
            user = self.scope['user']
            message = await self.save_message(user, self.conversation_id, content)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': message.id,
                    'content': content,
                    'sender_id': str(user.id),
                    'sender_name': user.full_name,
                    'created_at': message.created_at.isoformat(),
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def is_participant(self, user, conversation_id):
        from .models import Conversation
        return Conversation.objects.filter(id=conversation_id, participants=user).exists()

    @database_sync_to_async
    def save_message(self, user, conversation_id, content):
        from .models import Message, Conversation
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.save()  # update updated_at
        return Message.objects.create(
            conversation=conversation,
            sender=user,
            content=content
        )
