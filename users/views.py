import threading
from django.http import HttpResponse
from django.shortcuts import render
from users.models import  User, UserAdvancedFilter
from users.serializers import (
    SignUpSerializer,
    UserAdvancedFilterSerializer,
)
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import permissions
from django.db.models import Q
from utils.helpers import generateAPIResponse, generateUserOTP, validateOTPCode
from utils.tasks import send_email


commonFilters = [
    "sexual_orientation",
    "what_you_are_looking_for",
    "relationship_status",
    # "interests",
    # "bio",
    "school",
    # "company_name",
    # "work_title",
    "language",
    "drink",
    "drug",
    "kids",
    "introvert",
    "educationLevel",
    "relationshipGoal",
    "starSign",
    "pets",
    "religion",
    "ethnicity"
]
def implementAdvancedFilter(users, user):

    filter_conditions = Q()
    advancedFilter = UserAdvancedFilter.objects.filter(id = user.advancedFilterValues.id)

    for field in commonFilters:
        values = advancedFilter.values_list(field, flat=True)
        for value in values:
            if value:
                filter_conditions |= Q(**{f"{field}__icontains": value})
        
    filteredUsers = users.filter(filter_conditions)
    return filteredUsers





class ImplementAdavancedFilterView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request,email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return generateAPIResponse({}, "User not found", status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(
            ~Q(id = user.id)
        )
        filteredUsers = implementAdvancedFilter(users,user)
        return generateAPIResponse(
            SignUpSerializer(filteredUsers, many = True).data,
            "Users filtered successfully",
            status=status.HTTP_200_OK
        )


class RemoveAdvancedFilterField(APIView):
    def patch(self, request):
        user = request.user
        advancedFilter = UserAdvancedFilter.objects.get(id = user.advancedFilterValues.id)
        identifier = request.data.get("identifier")
        setattr(advancedFilter, identifier, "")
        advancedFilter.save()
        user.advancedFilterValues = advancedFilter

        return generateAPIResponse(
            SignUpSerializer(user).data,
            "Advanced filter removed successfully",
            status=status.HTTP_200_OK
        )





class LoginUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").lower()
        user = User.objects.filter(email=email)
        if user.exists() and not user[0].is_active:
            return Response(
                data={
                    "message":"Sorry User account is not activated",
                    "pending":True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(
            username=request.data.get("email"), password=request.data.get("password")
        )

        if user is not None:
            
            data={
                "user":SignUpSerializer(user).data,
                "token":user.auth_token.key
            }
            
            return generateAPIResponse(data,"User login successful", status=status.HTTP_200_OK)
            
        return Response(
            data={
                "message": "User Credentials are not correct",
            },
            status=status.HTTP_404_NOT_FOUND,
        )



class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email", "").lower()
        data = {
            "email":email,
            "phone_number":request.data.get("phone_number"),
            "password":"DEFAULT_PASSWORD@1"
        }
        s = SignUpSerializer(data=data)
        if User.objects.filter(email = email).exists():
            return Response(
                data ={
                    "message":"User with this email already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = request.data.get("phone_number", "")
        if not phone_number or len(phone_number) < 3:
            return Response(
                data ={
                    "message":"Phone number not valid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(phone_number = phone_number).exists():
            return Response(
                data ={
                    "message":"User with this phone already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if s.is_valid():
            s.save()

            user = User.objects.get(email=email)
            user.is_active= True
            user.save()


            return generateAPIResponse(s.data,"", status.HTTP_201_CREATED)
            
        return Response(data={"message": s.errors}, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email', "").lower()

        user = User.objects.filter(email=email)

        if user.exists():
            user = user.first()
            user.set_password(password)
            user.save()
            serializer = SignUpSerializer(user)
            return generateAPIResponse(serializer.data,"Password updated successfully", status.HTTP_201_CREATED)
        
        return generateAPIResponse({},"User not found", status.HTTP_404_NOT_FOUND)
        



class UpdateUserProfileImageView(APIView):
    permission_classes = [permissions.AllowAny]
    def patch(self, request):
        email = request.data.get("email", "").lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            return generateAPIResponse({},"User not found", status.HTTP_404_NOT_FOUND)
        files = request.data
        for file in files:
            if file != "email":
                update_index = file[-1]
                if update_index == "0":
                    user.first_profile_image = None
                if update_index == "1":
                    user.second_profile_image = None
                
                if update_index == "2":
                    user.third_profile_image = None
                
                if update_index == "3":
                    user.fourth_profile_image = None
                
                if update_index == "4":
                    user.fifth_profile_image = None
                

            user.save()
            
        userSerializer = SignUpSerializer(user)
        return generateAPIResponse(userSerializer.data,"User Image updated successfully", status.HTTP_200_OK)
    
    def post(self, request):
        email = request.data.get("email", "").lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            return generateAPIResponse({},"User not found", status.HTTP_404_NOT_FOUND)
        files = request.FILES
        for file in files:
            update_index = file[-1]
            if update_index == "0":
                user.first_profile_image = files.get(file)
            if update_index == "1":
                user.second_profile_image = files.get(file)
            
            if update_index == "2":
                user.third_profile_image = files.get(file)
            
            if update_index == "3":
                user.fourth_profile_image = files.get(file)
            
            if update_index == "4":
                user.fifth_profile_image = files.get(file)
            

            user.save()
            
        userSerializer = SignUpSerializer(user)
        
        return generateAPIResponse({
            "user":userSerializer.data,
            "token":user.auth_token.key
            },  "User Image updated successfully", status.HTTP_200_OK)

class UpdateUserDataView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email", "").lower()
        data = request.data
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist as e:
            return generateAPIResponse({},"User not found", status.HTTP_404_NOT_FOUND)
        
        del data["email"]
        serializer = SignUpSerializer(instance=user,  partial=True, data=data)


        if serializer.is_valid():
            serializer.save()
            filterSerializer = UserAdvancedFilterSerializer(instance=user.advancedFilterValues, partial=True, data=data)
            if filterSerializer.is_valid():
                filterSerializer.save()
            return generateAPIResponse(SignUpSerializer(user).data,"User data updated successfully", status.HTTP_200_OK)
        

        return Response(data={"message": "Error updating users credentials"}, status=status.HTTP_400_BAD_REQUEST)
    


class GetUserMatchView(APIView):
    def get(self, request):
        user = request.user
        users = User.objects.filter(
            Q(
                ~Q(gender = user.gender)
                |
                Q(country__icontains = user.country)
                |
                Q(state__icontains = user.state)
            )
        ).filter(~Q(id = request.user.id )).distinct()
        

        return generateAPIResponse(
            SignUpSerializer(users, many=True).data,
            "User retrieved successfully",
            status=status.HTTP_200_OK
        )

class Me(APIView):
    def get(self, request):
        user = request.user
        serializer = SignUpSerializer(user)
        return generateAPIResponse(serializer.data, "User fetched successfully", status.HTTP_200_OK)

class GetUserWithID(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist as e:
            return generateAPIResponse({},"User not found", status.HTTP_404_NOT_FOUND)

        serializer = SignUpSerializer(user)
        return generateAPIResponse(serializer.data, "User fetched successfully", status.HTTP_200_OK)

class GetUsersListView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(~Q(id = request.user.id)).order_by("-id")
        women = request.GET.get("women", "false")
        men = request.GET.get("men", "false")
        non_binary = request.GET.get("non_binary", "false")
        country = request.GET.get("country", "")
        ageMaximumRange = request.GET.get("ageMaximumRange", "")
        ageMinimumRange = request.GET.get("ageMinimumRange", "")


        if women == "true":
            users = users.filter(gender=settings.GENDERS[1])
        if men == "true":
            users = users.filter(gender=settings.GENDERS[0])
        if non_binary == "true":
            users = users.filter(gender=settings.GENDERS[2])
        if len(country):
            users = users.filter(country=country)
        
        if ageMaximumRange and ageMinimumRange:
            users = users.filter(age__range=(int(ageMinimumRange), int(ageMaximumRange)))


        
        if women != "true" and men != "true":
            ## USE USER PROFILE TO FILTER GENDER

            ##if user is looking for men
            if request.user.what_you_are_looking_for ==settings.LOOKINGFOR[0]:
                users = users.filter(gender=settings.GENDERS[0])
            
            ##if user is looking for women
            if request.user.what_you_are_looking_for ==settings.LOOKINGFOR[1]:
                users = users.filter(gender=settings.GENDERS[1])
            ##if user is looking for both
            if request.user.what_you_are_looking_for ==settings.LOOKINGFOR[2]:
                users = users.filter(gender=settings.GENDERS[2])
        





        serializer = SignUpSerializer(users, many=True)
        return generateAPIResponse(serializer.data, "Users list fetched successfully", status.HTTP_200_OK)

class IncreaseUserViewsCountView(APIView):
    def patch(self, request):
        user_id = request.data.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except:
            return generateAPIResponse({}, "User not found", status.HTTP_400_BAD_REQUEST)
        
        user.profile_views = user.profile_views + 1
        user.save()
        return generateAPIResponse({}, "User views count increased successfully", status.HTTP_200_OK)
    


class UpdateUserAdvancedFilterFieldView(APIView):
    permission_classes =[permissions.AllowAny]
    def post(self, request):
        user = request.user
        email = request.data.get('email')
        data = request.data


        try:
            user = User.objects.get(email=email)
            
        except User.DoesNotExist as e:
            return generateAPIResponse({},"User not found", status.HTTP_404_NOT_FOUND)
        del data["email"]
        serializer = UserAdvancedFilterSerializer(instance=user.advancedFilterValues,  partial=True, data=data)
        user = SignUpSerializer(user)



        if serializer.is_valid():
            serializer.save()
            return generateAPIResponse(user.data,"User advanced filter data updated successfully", status.HTTP_200_OK)
        

        return Response(data={"message": "Error updating users credentials"}, status=status.HTTP_400_BAD_REQUEST)
    


class UpdatePassworAuthdView(APIView):
    def patch(self, request):
        oldPassword = request.data.get("oldPassword")
        newPassword = request.data.get("newPassword")
        user = request.user

        if not user.check_password(oldPassword):
            return generateAPIResponse({}, "Old password does not match", status.HTTP_401_UNAUTHORIZED)
        
        user.set_password(newPassword)
        user.save()
        return generateAPIResponse(SignUpSerializer(user).data,"Password updated", status.HTTP_201_CREATED)


class UpdateLocationView(APIView):
    def patch(self, request):
        user = get_user_model().objects.get(id = request.user.id)
        longitude = request.data.get("longitude")
        latitude = request.data.get("latitude")
        user.longitude = longitude
        user.latitude = latitude
        user.save()

        return generateAPIResponse(
            SignUpSerializer(user).data,
            "User location updated successfully",
            status.HTTP_200_OK
        )
class DeleteAccountView(APIView):
    def delete(self, request):
        user = request.user
        user.delete()
        return generateAPIResponse({}, "Account deleted successfully", status.HTTP_200_OK)
    
    



class SendUserActivationEmail(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            return generateAPIResponse({}, "User not found", status=status.HTTP_400_BAD_REQUEST)
        c = generateUserOTP(email)
        message = render_to_string("emails/activation.html", { "code":c, "name":f"{user.full_name}"})
        t = threading.Thread(target=send_email, args=("Verification required", message,[email]))
        t.start()
        
        
        return generateAPIResponse({"message":"OTP sent"}, "Gift sent", status.HTTP_200_OK)

class ActivateUserAccount(APIView):
    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            return generateAPIResponse({}, "User not found", status=status.HTTP_400_BAD_REQUEST)
        
        checkCode = validateOTPCode(code).get("type")
        
        if checkCode:
            user.emailActivated = True
            user.is_active = True
            user.save()
            return generateAPIResponse({"data":SignUpSerializer(user).data,"message":"Account activated"}, "Account activated", status.HTTP_200_OK)
        else:
            return generateAPIResponse({}, "Invalid OTP", status=status.HTTP_400_BAD_REQUEST)