import threading
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import permissions
from django.db.models import Q
from users.models import User
from users.serializers import SignUpSerializer
from .models import Like
from utils.helpers import generateAPIResponse, sendMobileNotification




def checkIfUserMatchAndSendNotification(liker, liking):
    isMatched = Like.objects.filter(
        Q(Q(liked_by=liking) & Q(liked=liker))
        &
        Q(Q(liked_by=liker) & Q(liked=liking))
        
    ).exists()
    
    if isMatched:
        sendMobileNotification(
        liking,
        f"You have a new match with {liker.full_name}"
        )
        
        sendMobileNotification(
            liker,
            f"You have a new match with {liking.full_name}"
        )



class UpdateLike(APIView):
    def patch(self,request):
        liker = request.user
        liking_id = request.data.get("liking_id")

        try:
            liking = User.objects.get(id=liking_id)
        except User.DoesNotExist:
            return generateAPIResponse({}, "User not found", status=status.HTTP_400_BAD_REQUEST)
        

        isLiked = Like.objects.filter(
            Q(liked_by=liker) & Q(liked=liking)
        )
        

        if isLiked.exists():
            isLiked.delete()
        else:
            Like.objects.create(liked_by=liker, liked=liking)
            sendMobileNotification(
                liking,
                f"You recieved a like from {liker.full_name}"
            )
        
        tr = threading.Thread(target=checkIfUserMatchAndSendNotification, kwargs={
            "liker": liker,
            "liking": liking
        })
        tr.start()
        serializer = SignUpSerializer(liker)
        return generateAPIResponse(serializer.data, "Like updated successfully", status=status.HTTP_200_OK)

