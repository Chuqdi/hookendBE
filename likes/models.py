from django.db import models

from users.models import User




class Like(models.Model):
    ## This is the user liking
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liking")
    ## This is the user been liked
    liked = models.ForeignKey(User,related_name="my_likes", on_delete=models.CASCADE)
    date_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.liked.email