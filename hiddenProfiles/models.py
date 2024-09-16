from django.db import models

from users.models import User





class HideProfile(models.Model):
    hidden_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles_i_hid")
    hidden_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles_hidden_from_i")
    date_hidden = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f"{self.hidden_by.first_name} hid profile from {self.hidden_from.first_name}"