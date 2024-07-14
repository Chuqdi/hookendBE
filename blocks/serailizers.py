from rest_framework.serializers import ModelSerializer
from .models import Block




class BlockSerializer(ModelSerializer):
    class Meta:
        model = Block
        fields ="__all__"