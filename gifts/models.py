from django.db import models
from users.models import User


class Gift(models.Model):
    giftType = models.CharField(max_length=25)
    user_recieving= models.ForeignKey(User, on_delete=models.CASCADE, related_name="gifts_recieved")
    user_sending= models.ForeignKey(User, on_delete=models.CASCADE, related_name="gifts_sent")
    is_claimed = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return super().__str__()