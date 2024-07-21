from django.urls import path

from deviceTokens.views import AddUserDeviceToken


urlpatterns = [
    path("add_token/", AddUserDeviceToken.as_view(), name="add_token")
]
