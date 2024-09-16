from .views import HideAndGetProfile
from django.urls import path


urlpatterns = [
    path("get_hid", HideAndGetProfile.as_view())
]
