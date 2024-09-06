
from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from likes.models import Like
from users.models import User
from utils.helpers import sendMobileNotification
from utils.payment import generateSignatures
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


class Test(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        user1 = User.objects.get(email="morganhezekiah111@gmail.com")
        # user2 = User.objects.get(email="morganhezekiah123@gmail.com")
        user2 = User.objects.get(email="morganhezekiah123@gmail.com")
        
        firstLike = Like.objects.filter(liked_by = user1, liked=user2)
        secondLike = Like.objects.filter(liked_by = user2, liked=user1)
        
        if firstLike.exists() and secondLike.exists():
            print("match")
        
        
        
        
        return Response({"message":"Notification sent"}, status=status.HTTP_200_OK)


ROOT_URL="api/v1/"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("test", Test.as_view(), name="test"),
    path(ROOT_URL +"users/", include("users.urls")),
    path(ROOT_URL +"likes/", include("likes.urls")),
    path(ROOT_URL +"payments/", include("payments.urls")),
    path(ROOT_URL +"blocks/", include("blocks.urls")),
    path(ROOT_URL +"reports/", include("reports.urls")),
    path(ROOT_URL +"chats/", include("chats.urls")),
    path(ROOT_URL +"deviceTokens/", include("deviceTokens.urls")),
    path(ROOT_URL +"notifications/", include("notifications.urls")),
    path(ROOT_URL +"gifts/", include("gifts.urls")),
    path(ROOT_URL +"likedPhotos/", include("likedPhotos.urls")),
    
]
