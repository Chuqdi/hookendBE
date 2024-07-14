from django.db import models

from users.models import User



class Block(models.Model):
    blocked_by = models.ForeignKey(User, related_name="users_blocked", on_delete=models.CASCADE)
    blocking = models.ForeignKey(User, related_name="users_who_blocked_me", on_delete=models.CASCADE)
    reason = models.CharField(max_length=600, null=True, blank=True,)
    date_blocked = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.blocked_by.email
