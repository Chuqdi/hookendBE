from django.urls import path

from chats.views import DeleteUsersChatView, GetUserChatMessagesView

urlpatterns = [
    path("get_messages/", GetUserChatMessagesView.as_view(),),
    path("delete_chat/<reciever_id>/", DeleteUsersChatView.as_view())
]
