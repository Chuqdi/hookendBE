from django.urls import path
from .views import BlockUserView


urlpatterns = [
    path("block_user/", BlockUserView.as_view(), name="block_user")
]
