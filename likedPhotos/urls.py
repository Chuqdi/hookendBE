from .views import GetUserLikedPhotos
from django.urls import path

urlpatterns = [
    path("get", GetUserLikedPhotos.as_view(),),
]
