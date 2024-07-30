from .views import GetUserNotificationsView
from django.urls import path



urlpatterns = [
    path("get/", GetUserNotificationsView.as_view(),),
    path("create_comment/",GetUserNotificationsView.as_view(),)
]
