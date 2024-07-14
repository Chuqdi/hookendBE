from django.db import models

from users.models import User




class Report(models.Model):
    reported_by = models.ForeignKey(User, related_name="users_reported", on_delete=models.CASCADE)
    reporting = models.ForeignKey(User, related_name="users_who_reported_me", on_delete=models.CASCADE)
    reason = models.CharField(max_length=600, null=True, blank=True,)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.reported_by.email
