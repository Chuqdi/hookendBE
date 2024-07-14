from .models import AdvancedFilter, BoostedProfile, Premium, PremiumHooked, WildFeature
from rest_framework import serializers




class BoostedProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoostedProfile
        fields = "__all__"


class PremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premium
        fields = "__all__"


class PremiumHookedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumHooked
        fields = "__all__"

class WildFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WildFeature
        fields = "__all__"


class AdvancedFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedFilter
        fields = "__all__"