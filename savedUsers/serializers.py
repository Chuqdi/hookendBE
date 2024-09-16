
from rest_framework import serializers
from .models import SavedUser

class SavedUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields ="__all__"
        model = SavedUser
        
        