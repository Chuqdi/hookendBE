from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.


class SavedUser(models.Model):
    savedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_who_i_saved")
    saving = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_who_saved_me")
    date_saved = models.DateField( default=timezone.now)
    
    def __str__(self) -> str:
        return self.savedBy.email
    