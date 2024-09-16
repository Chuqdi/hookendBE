from users.serializers import SignUpSerializer
from .models import HideProfile
from rest_framework.serializers import ModelSerializer


class HideProfileSerializer(ModelSerializer):
    class Meta:
        model = HideProfile
        fields = "__all__"