import json
from channels.generic.websocket import AsyncWebsocketConsumer

import datetime
import pytz


def get_current_time():
    tz = pytz.timezone("Asia/Almaty")
    return datetime.datetime.now(tz).strftime('%H:%M:%S')


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope["user"].first_name

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        time_sent = get_current_time()

        await self.send(text_data=json.dumps({
            "message": message,
            "user": user,
            "send_time": time_sent,
        }))
