import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Chat, Message

class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):  
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = f"chat_{self.chat_box_name}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def create_message(self, owner: User, text: str):
        chat = Chat.objects.get(name=self.chat_box_name)
        message = Message(owner=owner, chat=chat, text=text)
        message.received = True
        message.save()
        return message

    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json["message"]
        username = text_data_json["username"]
        message = await self.create_message(self.scope['user'], text)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message.text,
                "username": username,
                "received": str(bool(message.received)).lower()
            },
        )
        

    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        #send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )
    
