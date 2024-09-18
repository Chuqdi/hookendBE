
from channels.generic.websocket import JsonWebsocketConsumer,AsyncConsumer, AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync

from chats.models import Chat
from chats.serializers import ChatSerializer
from deviceTokens.models import DeviceToken
from users.models import User
import json
from firebase_admin import messaging
from utils.helpers import convert_base64_to_image





class OnlineStatus(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

        self.user_room_name = "online_status"

        async_to_sync(self.channel_layer.group_add)(
            self.user_room_name,
            self.channel_name
        )
    def receive(self, text_data=None, bytes_data=None, **kwargs):
        content = json.loads(text_data)

        user_id = content.get("user_id")
        isOnline = content.get("isOnline")

        try:
            user = User.objects.get(id=user_id)
            user.isOnline = isOnline
            user.save()
        except:
            pass

        async_to_sync(
            self.channel_layer.group_send
        )(
            self.user_room_name,
            {
                "type":"onlineStatus.update",
                "data":{"user_id":user_id,"isOnline":isOnline}
            }
        )
    def onlineStatus_update(self, event):
        user_id = event["data"]["user_id"]
        isOnline=event["data"]["isOnline"]
        data={"user_id":user_id,"isOnline":isOnline}

        self.send_json(data)
    

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user_room_name,
            self.channel_name
        )
        return super().disconnect(code)
    








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

        if content.get("message_file") :
            reciever_id = content["reciever_id"]
            sender_id = content["sender_id"]



            sender= User.objects.get(id =sender_id)
            reciever= User.objects.get(id =reciever_id)
            
            file =convert_base64_to_image(content.get("message_file"))
            

            chat = Chat.objects.create(
                sender = sender,
                reciever=reciever,
                message_file=file,
                message_type="image"

            )
            

                
        
            
            serializer = ChatSerializer(chat)
           

        else:
            reciever_id = content["reciever_id"]
            sender_id = content["sender_id"]
            message = content["message"]



            sender= User.objects.get(id =sender_id)
            reciever= User.objects.get(id =reciever_id)
            
          
            chat = Chat.objects.create(
                sender = sender,
                reciever=reciever,
                message=message,

            )
            serializer = ChatSerializer(chat)

        try:
            user_token = DeviceToken.objects.get(user = reciever)


            n_message = messaging.Message(
            notification=messaging.Notification(
                title="Notification",
                body=f"You recieved a message from "+sender.full_name,
            ),
            token=user_token.token.strip(),
        )
            messaging.send(n_message)

        except Exception as  e:
            pass
        async_to_sync(
            self.channel_layer.group_send
        )(
            self.user_room_name,
            {
                "type":"chat.user",
                "data":serializer.data
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
    






