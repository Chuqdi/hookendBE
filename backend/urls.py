
from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from users.models import User
from utils.helpers import sendMobileNotification
from utils.payment import generateSignatures
from rest_framework.response import Response
from rest_framework import status

class Test(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        sendMobileNotification(
            user = User.objects.get(email="morganhezekiah111@gmail.com"),
            messageText = "Test Notification",
            # data={"key1":"value1", "key2":"value2"}
        )
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
]
