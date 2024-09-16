from rest_framework.views import APIView
from users.models import User
from .models import HideProfile
from .serializers import HideProfileSerializer
from utils.helpers import generateAPIResponse
from rest_framework import status




class HideAndGetProfile(APIView):
    def get(self, request, *args, **kwargs):
        hidden_by = request.user 
        hiddenProfiles = HideProfile.objects.filter(
            hidden_by = hidden_by
        )
        serializer = HideProfileSerializer(hiddenProfiles, many=True)
        
        
        return generateAPIResponse(data=serializer.data, message="Hidden profiles retrived", status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        hidden_by = request.user
        hidden_from = request.data.get("hidden_from")
        
        try:
            hidden_from = User.objects.filter(phone_number = hidden_from)
        except User.DoesNotExist:
            return generateAPIResponse({}, "User not found", status=status.HTTP_400_BAD_REQUEST)
        
        hidden_from = hidden_from.last()
        
        if HideProfile.objects.filter(hidden_by=hidden_by, hidden_from=hidden_from).exists():
            HideProfile.objects.filter(
                hidden_by=hidden_by, hidden_from=hidden_from
            ).delete()
        else:
            HideProfile.objects.create(
                hidden_by=hidden_by,
                hidden_from=hidden_from
            )
        
        
        return generateAPIResponse({}, "Profile hidden successfully", status=status.HTTP_200_OK)
