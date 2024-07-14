import threading
from django.http import HttpResponse
from django.shortcuts import render
from users.models import  User
from users.serializers import (
    SignUpSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import permissions
from django.db.models import Q
from utils.helpers import generateAPIResponse, generateUserOTP







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
            print(
                SignUpSerializer(user).data
            )
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
            c = generateUserOTP(email)
            # message = render_to_string("emails/activation.html", { "code":c, "name":f"{first_name} {last_name}"})
            # t = threading.Thread(target=send_email, args=("Verification required", message,[email]))
            # t.start()



            # message = render_to_string("emails/welcome.html", { "name":f"{first_name} {last_name}"})
            # t = threading.Thread(target=send_email, args=(f"Welcome {first_name}", message,[email]))
            # t.start()

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
        return generateAPIResponse(userSerializer.data, "User Image updated successfully", status.HTTP_200_OK)
    
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
                print("here")
                user.third_profile_image = files.get(file)
            
            if update_index == "3":
                user.fourth_profile_image = files.get(file)
            
            if update_index == "4":
                user.fifth_profile_image = files.get(file)
            

            user.save()
            
        userSerializer = SignUpSerializer(user)
        return generateAPIResponse(userSerializer.data, "User Image updated successfully", status.HTTP_200_OK)

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
            return generateAPIResponse(serializer.data,"User data updated successfully", status.HTTP_200_OK)
        

        return Response(data={"message": "Error updating users credentials"}, status=status.HTTP_400_BAD_REQUEST)
    


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
            users = users.filter(gender="female")
        if men == "true":
            users = users.filter(gender="male")
        if non_binary == "true":
            users = users.filter(gender="non_binary")
        if len(country):
            users = users.filter(country=country)




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