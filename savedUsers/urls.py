from django.urls import path
from .views import SaveUserAndGetSavedUsers

urlpatterns = [
    path("save_get_saved_users", SaveUserAndGetSavedUsers.as_view(),),
]
