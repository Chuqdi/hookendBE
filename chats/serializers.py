from users.serializers import SignUpSerializer
from .models import Chat
from rest_framework.serializers import ModelSerializer



class ChatSerializer(ModelSerializer):
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