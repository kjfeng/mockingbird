# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Thread, ChatMessage
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        other_user = self.scope['url_route']['kwargs']['room_name']
        this_user = self.scope['user']
        thread_obj = await self.get_thread(this_user, other_user)
        self.thread_obj = thread_obj
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room

        # Join room group
        await self.channel_layer.group_add(
            self.chat_room, #unique chatroom to the two users
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        if text_data is not None:
            loaded_dict_data = json.loads(text_data)
            msg = loaded_dict_data.get('message')
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
                await self.create_chat_message(msg)
            response = json.dumps({
                'message': msg,
                'username': username
            })
            

            # Broadcasts message to be sent to group
            await self.channel_layer.group_send(
                self.chat_room, 
                {
                    'type': 'chat_message',
                    'message': response
                }
            )

    # Receive message from room group (done by group_send)
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(message)

    # Gets the chat message thread or creates a new one (wrapper for chat messages)
    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, msg):
        thread_obj = self.thread_obj
        user = self.scope['user']
        return ChatMessage.objects.create(thread=thread_obj, user=user, message=msg)