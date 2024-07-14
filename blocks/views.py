from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status

from users.serializers import SignUpSerializer
from .models import Block
from users.models import User
from utils.helpers import generateAPIResponse



class BlockUserView(APIView):
    def patch(self, request):
        blocked_by = request.user
        blocking_id = request.data.get('blocking_id')
        reason = request.data.get('reason')

        try:
            blocking = User.objects.get(id=blocking_id)
        except User.DoesNotExist as e:
            return generateAPIResponse({}, "User not found", status.HTTP_400_BAD_REQUEST)
        
        block = Block.objects.get_or_create(
            blocking=blocking,
            blocked_by=blocked_by,
            reason=reason,
        )
        user  = SignUpSerializer(
            blocked_by,
        )

        return generateAPIResponse(user.data, "User blocked successfully", status.HTTP_201_CREATED)

