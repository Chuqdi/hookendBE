from users.serializers import SignUpSerializer
from .models import Chat
from rest_framework.serializers import ModelSerializer



class ChatSerializer(ModelSerializer):
    sender = SignUpSerializer(
        many=False,
        read_only=True,
    )
    reciever = SignUpSerializer(
        many=False,
        read_only=True,
    )
    class Meta:
        model = Chat
        fields = [
            "sender",
            "reciever",
            "message_type",
            "message",
            "message_file",
            "date_sent",
            "is_read",
            "is_deleted"
        ]