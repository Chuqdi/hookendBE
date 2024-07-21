from django.db import models

from users.models import User




class DeviceToken(models.Model):
    token = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email