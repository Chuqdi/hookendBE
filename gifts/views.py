from django.shortcuts import render
from gifts.models import Gift
from notifications.models import Notification
from users.models import User
from firebase_admin import messaging
from deviceTokens.models import DeviceToken
from utils.helpers import generateAPIResponse, sendMobileNotification
from rest_framework.views import APIView
from rest_framework import status
from .serializer import GiftSerializer
from users.serializers import SignUpSerializer





class RedeemCoinView(APIView):
    def post(self, request):
        user = request.user
        coin = Gift.objects.filter(
            user_recieving=user
        ).filter(giftType="COIN")
        coin.delete()
        return generateAPIResponse({}, "User coins retrieved", status=status.HTTP_200_OK)
        
        

class GetOrSendGiftsView(APIView):
    def get(self, request):
        user = request.user
        gifts = Gift.objects.filter(
            user_recieving = user
        )
        giftsSerializer = GiftSerializer(
            gifts,
            many=True
        )
        
        return generateAPIResponse(giftsSerializer.data, "Gifts fetched successfully", status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        recieving_user = request.data.get("recieving_user_id")
        
        try:
            recieving_user = User.objects.get(id=recieving_user)
        except User.DoesNotExist:
            return generateAPIResponse({}, "Recieving user not found", status=status.HTTP_400_BAD_REQUEST)
        giftType = request.data.get("giftType")
        
        gift = Gift.objects.create(
            giftType = giftType,
            user_recieving = recieving_user,
            user_sending = user
        )
        giftTypeLower = giftType.lower()
        
        
     
        sendMobileNotification(
                recieving_user,
               f"{user.full_name} sent you a {giftTypeLower} ",
               data={
                   "screen":"Notifications"
               }
            )
        n = Notification.objects.create(
            notification_sender= request.user,
            notified_users = recieving_user,
            message = f"{user.full_name} sent you a {giftTypeLower}",
            notification_type = request.data.get("giftType")
        )
        
        if giftType == "COIN":
            user.coin = user.coin - 1
        if giftType == "TEDDY":
            user.teddy = user.teddy - 1
        if giftType == "ROSE":
            user.rose = user.rose - 1
        user.save()
            
            
            
        
        userSerializer = SignUpSerializer(
            user,
        )
        
        return generateAPIResponse(userSerializer.data, "Gift sent", status.HTTP_200_OK)

        
