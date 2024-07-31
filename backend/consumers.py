
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from chats.models import Chat
from users.models import User
import json

from utils.helpers import convert_base64_to_image










class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

        sender_id = int(self.scope['url_route']['kwargs']['sender_id'])
        reciever_id = int(self.scope['url_route']['kwargs']['reciever_id'])

        self.user_room_name = f'user_room_'

        if sender_id > reciever_id:
            self.user_room_name =f'{self.user_room_name}{sender_id}{reciever_id}'
        else:
            self.user_room_name =f'{self.user_room_name}{reciever_id}{sender_id}'





        

        
        async_to_sync(self.channel_layer.group_add)(
            self.user_room_name,
            self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None, **kwargs):
        content = json.loads(text_data)

        if content.get("image") :
            reciever_id = content["reciever_id"]
            sender_id = content["sender_id"]



            sender= User.objects.get(id =sender_id)
            reciever= User.objects.get(id =reciever_id)
            data ={
                "reciever":reciever,
                "sender":sender,
                "image": convert_base64_to_image(content.get("image")),
                "is_image":True
            }

            # chat =ChatSerializer(data=data)
            if chat.is_valid():
                chat.save()
            else:
                chat.errors
            chat = chat.data


        else:
            reciever_id = content["reciever_id"]
            sender_id = content["sender_id"]
            message = content["message"]



            sender= User.objects.get(id =sender_id)
            reciever= User.objects.get(id =reciever_id)

            chat =Chat.objects.create(
                reciever=reciever,
                sender=sender,
                message=message
            )

        async_to_sync(
            self.channel_layer.group_send
        )(
            self.user_room_name,
            {
                "type":"chat.user",
                # "data":ChatSerializer(chat).data
            }
        )
    
    # def receive_json(self, content, **kwargs):

    

    def chat_user(self, event):
        data = event["data"]

        self.send_json(data)


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user_room_name,
            self.channel_name
        )
        return super().disconnect(code)
    






