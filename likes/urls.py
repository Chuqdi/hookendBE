from django.urls import path
from .views import UpdateLike


urlpatterns = [
    path("update_like/", UpdateLike.as_view())
]
