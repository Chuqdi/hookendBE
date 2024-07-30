from rest_framework.serializers import ModelSerializer

from gifts.models import Gift


class GiftSerializer(ModelSerializer):
    class Meta:
        model = Gift
        fields = "__all__"