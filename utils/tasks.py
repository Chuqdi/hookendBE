import threading
from celery import shared_task
from botMessages.models import BotMessage
from deviceTokens.models import DeviceToken
from roles.models import Distrubution, InterviewQuestion, Role
from usermessages.models import UserMessage
from utils.helpers import generateSecureEmailCredentials
from django.db.models import Count
from firebase_admin import messaging
import random
from .EmailSender import SendEmail, send_activation_email
from users.models import User
from django.template.loader import render_to_string
from django.conf import settings
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage




JOB_APPLICATION_UPDATE ="Your job application update."


BOT_ACCOUNT_EMAILS = [
   "apextalents@yahoo.com",
   "leonstark@yahoo.com",
   "greenleaf@yahoo.com",
   "berkleyduffy@yahoo.com",
   "nexusstaffs@yahoo.com"
]


def botMessages(first_name:str, last_name:str, number):
    name = f"{first_name} {last_name}"
    message =""
    if number == 0:
        message= f"""Your resume stood out. We'd like to schedule an interview with you next week.
        Please reply immediately if you are interested as we have other candidates on our list.
        """
    elif number == 1:
        message= f"""We'd like to schedule an interview with you next week. Please let us know your availability.
        """
    elif number == 2:
        message= f"""Your application impressed us. When could you come in for an interview anytime soon?
        """
    elif number == 3:
        message= f"""We look forward to discussing how your skills align with our team’s goals. When are you available for an interview?
        """
    else:
        message= f"""Your background is impressive. We are eager to discuss how your skills can benefit our team during your interview.
        When are you free?
        """
    return message


# @shared_task
# def sendMessageTo14():
#     users = User.objects.all()
#     users = users.filter(number_of_distrubution_this_month__gte=1).filter(number_of_distrubution_this_month__lte=4).annotate(bot_messages_count=Count('bot_messages')).filter(bot_messages_count__lt=6)
#     for u in users:
#         try:
#             random_email = random.choice(BOT_ACCOUNT_EMAILS)
#             sender = User.objects.get(email=random_email)
#             random_num = random.randint(0, 4)
#             message = botMessages(u.first_name, u.last_name, random_num)
#             UserMessage.objects.create(
#                 message=message,
#                 sender = sender,
#                 reciept = u,
#             )
#             BotMessage.objects.create(user = u)
#         except Exception as e:
#             pass



# @shared_task
# def sendMessageTo59():
#     users = User.objects.all()
#     users = users.filter(number_of_distrubution_this_month__gte=5).annotate(bot_messages_count=Count('bot_messages')).filter(bot_messages_count__lt=6)
#     for u in users:
#         try:
#             random_email = random.choice(BOT_ACCOUNT_EMAILS)
#             sender = User.objects.get(email=random_email)
#             random_num = random.randint(0, 4)
#             message = botMessages(u.first_name, u.last_name, random_num)
#             UserMessage.objects.create(
#                 message=message,
#                 sender = sender,
#                 reciept = u,
#             )
#             BotMessage.objects.create(user = u)
#         except Exception as  e:
#             pass




@shared_task
def test():
    print("Yes on the task")









@shared_task
def sendUserActivationEmail(email, domain):
    user = User.objects.get(email=email)
    secureEmailCredentials = generateSecureEmailCredentials(user)
    token = secureEmailCredentials.get("token")
    uidb64 = secureEmailCredentials.get("uidb64")
    
    urlPath = f"{domain}/api/v1/users/activate_account/{token}/{uidb64}/"
    send_activation_email(
        user=user,
        template="emails/user_account_activation.html",
        urlPath=urlPath,
        subject="Account Email Activation",
    )



@shared_task
def actionNotificationEmail(message, to, title=""):
    template = render_to_string(
        "emails/action_notification.html", {"message": message, "title": title}
    )

    s = SendEmail(template=template, subject="Action Notification", to=(to,))





@shared_task(serializer='pickle')
def saveInterviewVideo(video, question, role_id):
    role = Role.objects.get(id=role_id)
    iq = InterviewQuestion.objects.create(
            question = question,
            video = video,
        )
    role.interviewQuestions.add(iq)
    role.save()



@shared_task
def send_email( subject, message, recipient_list, ):
    
    message = EmailMessage(subject, message,  settings.DEFAULT_FROM_EMAIL,recipient_list)
    message.content_subtype = 'html' 
    message.send()
    



@shared_task
def update_db_monthly_distributions():
    users = User.objects.all()
    for user in users:
        if user.is_active:
            user.number_of_distrubution_this_month =0
            user.number_of_notifications_this_month = 0
            user.number_of_notifications_this_month = 0
            user.save()








def sendNotificationEmail(name, message, to):
    message = render_to_string("emails/message.html", { "name":name, "message":message})
    t = threading.Thread(target=send_email, args=("Account Notification", message,[to,]))
    t.start()




# @shared_task
# def sendUserRoleNotifications8Hours():
#     roles = Role.objects.all()

#     for r in roles.iterator():
#         user = User.objects.get(email=r.user.email)
#         d = Distrubution.objects.filter(user= user)
#         if d.count() > 0 :
#             if user.subscription.upper() == settings.SUBSCRIPTIONTYPES[0].upper():
#                 if user.number_of_notifications_this_month < 5:
#                     user.number_of_notifications_this_month = user.number_of_notifications_this_month + 1
#                     user.save()
#                     title =JOB_APPLICATION_UPDATE
#                     message ="An employer just viewed your CV📝"
#                     sendNotificationEmail(name=f"{user.first_name} {user.last_name}", message=message, to=user.email)
#                     r.view_count = int(r.view_count) + 1
#                     r.save()
                


#                     try:
#                         user_token = DeviceToken.objects.get(user = user)

#                         n_message = messaging.Message(
#                         notification=messaging.Notification(
#                             title=title,
#                             body=message,
#                         ),
#                         token=user_token.token.strip(),
#                     )
#                         messaging.send(n_message)
#                     except:
#                         pass
                




# @shared_task
# def sendUserRoleNotifications10Hours():
#     roles = Role.objects.all()


#     for r in roles.iterator():
#         user = User.objects.get(email=r.user.email)
#         d = Distrubution.objects.filter(user= user)
#         if d.count() > 0 :
#             if  user.subscription.upper() != settings.SUBSCRIPTIONTYPES[0].upper():
#                 title =JOB_APPLICATION_UPDATE
#                 message ="Multiple employers has viewed your CV📝"
#                 r.view_count = int(r.view_count) + 1
#                 r.save()
#                 sendNotificationEmail(name=f"{user.first_name} {user.last_name}", message=message, to=user.email)

#                 try:
#                     user_token = DeviceToken.objects.get(user = user)

#                     n_message = messaging.Message(
#                     notification=messaging.Notification(
#                         title=title,
#                         body=message,
#                     ),
#                     token=user_token.token.strip(),
#                 )
#                     messaging.send(n_message)
#                 except:
#                     pass
                





@shared_task
def sendABotMessageToUser(reciept_id):
    message =f""
    sender = User.objects.get(email="morganhezekiah123@gmail.com")
    reciept = User.objects.get(id = reciept_id)
    UserMessage.objects.create(message=message, reciept=reciept, sender=sender)

# @shared_task
# def sendUserSubscriptionrRequestNotification():
  
#     users = User.objects.all()
#     for user in users.iterator():
#         messages = [
#             "Your CV is gaining traffic. Upgrade your plan to improve your chances of distributing your CV to more employers and getting hired faster.",
#             ""
#         ]
#         distributions = Distrubution.objects.filter(user = user)
#         if distributions.count() > 0:
#             if user.subscription.upper() != settings.SUBSCRIPTIONTYPES[4].upper():
#                 title = JOB_APPLICATION_UPDATE
#                 message = "Your CV is gaining traffic🔥. Upgrade your plan to improve your chances of distributing your CV to more employers and getting hired faster."
#                 sendNotificationEmail(name=f"{user.first_name} {user.last_name}", message=message, to=user.email)

#                 try:
#                     user_token = DeviceToken.objects.get(user = user)

#                     n_message = messaging.Message(
#                     notification=messaging.Notification(
#                         title=title,
#                         body=message,
#                     ),
#                     token=user_token.token.strip(),
#                 )
#                     messaging.send(n_message)
#                 except:
#                     pass


