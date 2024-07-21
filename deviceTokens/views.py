from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from deviceTokens.models import DeviceToken




class AddUserDeviceToken(APIView):
    permission_classes = [permissions.IsAuthenticated ]
    def post(self, request):
        token = request.data.get("token")

        user = request.user

        tokenInstance, created = DeviceToken.objects.get_or_create(user = user)
        tokenInstance.token= token
        tokenInstance.save()

        
        return Response(status=status.HTTP_201_CREATED, data={
            "message":"Device token added successfully"
        })
