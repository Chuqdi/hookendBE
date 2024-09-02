from .models import LikedPhoto
from rest_framework import serializers


class LikedPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedPhoto
        fields = [
            "photo"
        ]