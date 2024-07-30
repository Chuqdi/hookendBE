from django.db import models

from users.models import User



class Notification(models.Model):
    message = models.TextField()
    notified_users = models.ForeignKey(User, on_delete=models.CASCADE , related_name="notifications_recieved" )
    notification_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_sent")
    # "TEDDY"|"ROSE"|"LIKE"|"COIN"
    notification_type = models.CharField(max_length=255)
    date_sent = models.DateTimeField(auto_now_add=True)
    likedPhoto = models.CharField(null=True, blank=True, max_length=255)
    
    
    def __str__(self) -> str:
        return super().__str__()
    