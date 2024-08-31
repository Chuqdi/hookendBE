from django.urls import path
from .views import GetMatchDateView, UpdateLike


urlpatterns = [
    path("update_like/", UpdateLike.as_view()),
    path("get_match_date/", GetMatchDateView.as_view(),)
]
