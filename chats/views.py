from django.shortcuts import render
from rest_framework.views import APIView

from users.models import User
from .models import Chat
from django.db.models import Q
from .serializers import ChatSerializer
from utils.helpers import generateAPIResponse
from rest_framework import status




class DeleteUsersChatView(APIView):
    def delete(self, request, reciever_id):
        user = request.user
        try:
            reciever = User.objects.get(id=reciever_id)
        except User.DoesNotExist:
            return generateAPIResponse({}, "User not found", status=status.HTTP_400_BAD_REQUEST)
        
        chat = Chat.objects.filter(
         Q(
                Q(
                Q(
                sender = user 
            )
            &
            Q(
                reciever = reciever
            )
            )

|
              Q(Q(
                sender = reciever 
            )
            &
            Q(
                reciever = user
            ))
       
         )
        )
        chat.delete()
        
        return generateAPIResponse({}, "Chat deleted successfully", status=status.HTTP_200_OK)

class GetUserChatMessagesView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        chat_messages = Chat.objects.filter(
            Q(sender=user) | Q(reciever=user),
        ).distinct()
        print("Here")

        serializers = ChatSerializer(chat_messages, many=True)
        return generateAPIResponse(serializers.data, "Chat messages fetched successfully", status.HTTP_200_OK)