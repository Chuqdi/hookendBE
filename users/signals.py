from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.models import AdvancedFilter, BoostedProfile, PremiumPlus, WildFeature, PremiumHooked
from .models import User, UserAdvancedFilter

@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        premiumPlus = PremiumPlus.objects.create()
        premiumHooked = PremiumHooked.objects.create()
        wildFeature = WildFeature.objects.create()
        advancedFilter = AdvancedFilter.objects.create()
        boostedProfile = BoostedProfile.objects.create()
        advancedFilterValues  = UserAdvancedFilter.objects.create()

        instance.premiumPlus = premiumPlus
        instance.premiumHooked = premiumHooked
        instance.wildFeature = wildFeature
        instance.advancedFilter = advancedFilter
        instance.advancedFilter = advancedFilter
        instance.boostedProfile = boostedProfile
        instance.advancedFilterValues = advancedFilterValues
        instance.save()