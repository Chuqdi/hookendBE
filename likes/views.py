import threading
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import permissions
from django.db.models import Q
from likedPhotos.models import LikedPhoto
from users.models import User
from users.serializers import SignUpSerializer
from .models import Like
from utils.helpers import generateAPIResponse, sendMobileNotification




def checkIfUserMatchAndSendNotification(liker, liking):
    firstLike = Like.objects.filter(liked_by = liker, liked=liking)
    secondLike = Like.objects.filter(liked_by = liking, liked=liker)
    isMatched = firstLike.exists() and secondLike.exists()
    
    if isMatched:
        sendMobileNotification(
        liking,
        f"""Sparks are flying! You and {liker.full_name} are a match.""",
        data={
            "screen":"Likes"
        }
        )
        
        sendMobileNotification(
            liker,
            f"""Sparks are flying! You and {liking.full_name} are a match.""",
              data={
            "screen":"Likes"
        }
        )



class UpdateLike(APIView):
    def patch(self,request):
        liker = request.user
        liking_id = request.data.get("liking_id")
        likedPhoto = request.data.get("likedPhoto", "")
        

        try:
            liking = User.objects.get(id=liking_id)
        except User.DoesNotExist:
            return generateAPIResponse({}, "User not found", status=status.HTTP_400_BAD_REQUEST)
        

        isLiked = Like.objects.filter(
            Q(liked_by=liker) & Q(liked=liking)
        )
        
            
            
        if likedPhoto:
            LikedPhoto.objects.create(user=liker, photo=likedPhoto)
        

        if isLiked.exists():
            # isLiked.delete()
            pass
        else:
            Like.objects.create(liked_by=liker, liked=liking, 
                                )
            sendMobileNotification(
                liking,
                f"{liker.full_name} liked your picture",
                  data={
            "screen":"Notifications"
        }
            )

        
        tr = threading.Thread(target=checkIfUserMatchAndSendNotification, kwargs={
            "liker": liker,
            "liking": liking
        })
        tr.start()
        serializer = SignUpSerializer(liker)
        return generateAPIResponse(serializer.data, "Like updated successfully", status=status.HTTP_200_OK)



class GetMatchDateView(APIView):
    def post(self, request):
        id = request.data.get("id")
        user = request.user
        
        try:
            matchUser = User.objects.get(id=id)
        except User.DoesNotExist as e:
            return generateAPIResponse({}, "User not found", status=status.HTTP_400_BAD_REQUEST)
        
        matches = Like.objects.filter(
            Q(Q(liked_by=user) & Q(liked=matchUser))
            |
            Q(liked_by=matchUser) & Q(liked=user)
        ).order_by("id")
        lastMatchDate = None
        if matches.exists():
            lastMatchDate = matches.last().date_liked
        return generateAPIResponse({"data":lastMatchDate, }, "Match date retrieved", status.HTTP_200_OK)
        
        
        
        