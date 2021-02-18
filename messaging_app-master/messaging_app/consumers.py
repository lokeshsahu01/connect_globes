import json
from channels.generic.websocket import AsyncWebsocketConsumer
from adduser.models import *
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            if Room.object.filter(room_name=self.room_name).exists():
                if Room.object.filter(room_name=self.room_name, allowed_users__contains=self.scope["user"].id).exists():
                    pass
            else:
                if '_' in self.room_name:
                    users = []
                    for i in self.room_name.split('_'):
                        users.append(User.objects.get(username=i).id)
                    Room(room_name=self.room_name, allowed_users=str(users)).save()

            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
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
        text_data_json = json.loads(text_data)
        text_data_json['type'] = 'chat_message'
        if Room.object.filter(room_name=text_data_json['room']).exists():
            if Room.object.filter(Q(allowed_users__contains=text_data_json['sender']) & Q(allowed_users__contains=text_data_json['receiver']), room_name=self.room_name).exists():
                pass
            else:
                room_obj = Room.object.get(room_name=text_data_json['room'])
                room_obj.allowed_users = str([text_data_json['sender'], text_data_json['receiver']])
            Messages(sender=User.objects.get(id=text_data_json['sender']),
                     receiver=User.objects.get(id=text_data_json['receiver']),
                     message=text_data_json['message']).save()

        await self.channel_layer.group_send(
            self.room_group_name, text_data_json
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))