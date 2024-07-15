from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.models import AdvancedFilter, BoostedProfile, Premium, WildFeature, PremiumHooked
from .models import User

@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        premium = Premium.objects.create()
        premiumHooked = PremiumHooked.objects.create()
        wildFeature = WildFeature.objects.create()
        advancedFilter = AdvancedFilter.objects.create()
        boostedProfile = BoostedProfile.objects.create()

        instance.premium = premium
        instance.premiumHooked = premiumHooked
        instance.wildFeature = wildFeature
        instance.advancedFilter = advancedFilter
        instance.advancedFilter = advancedFilter
        instance.boostedProfile = boostedProfile
        instance.save()