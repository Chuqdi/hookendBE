from django.db import models

from users.models import User



class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_chats")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recieved_messages")
    ##NOTE: text, audio, image
    message_type = models.CharField(max_length=30, default="text")
    message = models.TextField(null=True, blank=True)
    message_file = models.FileField(null=True, blank=True, upload_to="chat_message_files/")
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.sender.id}_{self.message}_{self.reciever.id}"
