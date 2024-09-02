from django.shortcuts import render
from .serializers import LikedPhotoSerializer
from .models import LikedPhoto
from rest_framework.views import APIView
from rest_framework import status
from utils.helpers import generateAPIResponse

class GetUserLikedPhotos(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        liked_photos = LikedPhoto.objects.filter(user=user)
        serializer = LikedPhotoSerializer(liked_photos, many=True)
        return generateAPIResponse(serializer.data, message="Liked photos retrieved",status=status.HTTP_200_OK)