from django.db import models

from users.models import User




class LikedPhoto(models.Model):
    photo = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)