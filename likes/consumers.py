
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class LikeLiveUpdateConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()


        self.user_room_name = f'like_room'
        
        async_to_sync(self.channel_layer.group_add)(
            self.user_room_name,
            self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None, **kwargs):
        content = json.loads(text_data)
        
        
        async_to_sync(
            self.channel_layer.group_send
        )(
            self.user_room_name,
            {
                "type":"chat.user",
                "data":content
            }
        )
    

    

    def chat_user(self, event):
        data = event["data"]

        self.send_json(data)


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user_room_name,
            self.channel_name
        )
        return super().disconnect(code)
    

