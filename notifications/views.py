from django.shortcuts import render
from rest_framework.views import APIView

from users.models import User
from .serializers import NotificationSerializer
from notifications.models import Notification
from utils.helpers import generateAPIResponse, sendMobileNotification
from rest_framework import status



class GetUserNotificationsView(APIView):
    def post(self, request):
        user = request.user
        notification_reciever_id = request.data.get('notification_reciever_id')
        comment = request.data.get('comment')
        likedPhoto= request.data.get('likedPhoto')
        
        
        try:
            notification_reciever = User.objects.get(id=notification_reciever_id)
        except:
            return generateAPIResponse({}, "Notification reciever not found", status=status.HTTP_400_BAD_REQUEST)
        
        
        
        notifications = Notification.objects.create(
            message= comment,
            notified_users= notification_reciever,
            notification_type="LIKE",
            likedPhoto=likedPhoto,
            notification_sender=user
        )
        
        sendMobileNotification(
                notification_reciever,
                f"{user.full_name} commentted on your image."
            )
        
        return generateAPIResponse(NotificationSerializer(notifications).data, "Notification created", status=status.HTTP_201_CREATED)
    def get(self, request):
        notifications=  Notification.objects.filter(
            notified_users = request.user
        )
        notificationsSerializer = NotificationSerializer(
            notifications,
            many=True
        )
        
        return generateAPIResponse(notificationsSerializer.data, "Notifcations retrieved", status=status.HTTP_200_OK)