from rest_framework.views import APIView
from users.models import User
from .models import SavedUser
from .serializers import SavedUserSerializer
from utils.helpers import generateAPIResponse
from rest_framework import status
from users.models import User



class SaveUserAndGetSavedUsers(APIView):
    def get(self, request, *args, **kwargs):
        savedBy = request.user
        savings = SavedUser.objects.filter(savedBy=savedBy)
        serializer = SavedUserSerializer(
            savings,
            many =True
        )
        
        return generateAPIResponse(data=serializer.data, message="Saved users retrieved", status=status.HTTP_200_OK)

    
    def post(self, request, *args, **kwargs):
        savedBy = request.user
        saving = request.data.get("saving")
        
        try:
            saving = User.objects.filter(id = saving)
        except:
            return generateAPIResponse(data={}, message="User not found", status=status.HTTP_400_BAD_REQUEST)
        
        saving = saving.first()
        
        if SavedUser.objects.filter(saving=saving, savedBy=savedBy).exists():
            SavedUser.objects.filter(saving=saving, savedBy=savedBy).delete()
        else:
            SavedUser.objects.create(
                saving=saving, savedBy=savedBy
            )
            
        
        return generateAPIResponse(
            data={}, message="User saved successfully", status=status.HTTP_200_OK
        )