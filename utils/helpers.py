import threading
from django.utils import timezone
from deviceTokens.models import DeviceToken
from utils.randomString import GenerateRandomString
from users.models import  User, UserEmailActivationCode
from datetime import timedelta
from firebase_admin import messaging
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from utils.TokenGenerator import generateToken
from django.conf import settings
from django.conf import settings
from datetime import datetime
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from math import radians, sin, cos, sqrt, atan2
import base64
import uuid
from django.core.files.base import ContentFile




def calculate_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    R = 6371.0  

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    
    return distance


def convert_base64_to_image(file_base64):

    format, imgstr = file_base64.split(';base64,')
    ext = format.split('/')[-1] 

    file_name = f"{uuid.uuid4().hex}.{ext}"

    try:
        decoded_file = base64.b64decode(imgstr)

        return ContentFile(decoded_file, name=file_name)
    except:
        return None

       


def generateAPIResponse(data, message, status):
    return Response(
                data={"data":data,"message":message},
                status=status,
            )


def send_email_here( subject, message, recipient_list, ):
    message = EmailMessage(subject, message,  settings.DEFAULT_FROM_EMAIL,recipient_list)
    message.content_subtype = 'html' 
    message.send()

    

def formatResumeDownloadLink(role_id):
    path = f"{settings.BACKEND_URL}api/v1/roles/download_role_data/{role_id}/"
    return path
     

def generateUserOTP(email):
    user = User.objects.get(email=email)
    code = GenerateRandomString.randomStringGenerator(6).upper()
    c = UserEmailActivationCode.objects.create(user=user, code =code)
    return code


def generateSecureEmailCredentials(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = generateToken.make_token(user)

    return {"uidb64": uidb64, "token": token}


def sendMobileNotification(user, messageText,data={}):
        try:
            user_token = DeviceToken.objects.get(user = user)
            n_message = messaging.Message(
            notification=messaging.Notification(
                title="Notification",
                body=messageText,
            ),
            token=user_token.token.strip(),
            # data=data
        )
            messaging.send(n_message)
            print("Notification senf")
        except Exception as e:
            print(e)

def validateOTPCode(code):
    
        c = UserEmailActivationCode.objects.filter(code = code)

        if not c.exists():
            return {
                "message":"OTP does not exist",
                "type":False
            }

        code = c[0]
        if (code.date_created + timedelta(minutes=30)) < timezone.now():
            code.delete()
            return {
                "message":"OTP has expired",
                "type":False,
            }
        code.delete()

        return  {
                "message":"OTP is valid",
                "type":True,
                "code":code
            }







