from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.helpers import sendMobileNotification
from .models import Chat

# @receiver(post_save, sender=Chat) 
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         sendMobileNotification(
#             instance.reciever,
#             f"Chat message from {instance.sender.full_name}.",
#             data={"screen":"Chat"}
#         )