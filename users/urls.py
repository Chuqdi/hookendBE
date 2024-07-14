from django.urls import path
from .views import GetUserWithID, IncreaseUserViewsCountView, Me, RegisterUserView, UpdatePasswordView, UpdateUserDataView, LoginUserView, UpdateUserProfileImageView, GetUsersListView


urlpatterns = [
    path("me/", Me.as_view(), name="me"),
    path("register/", RegisterUserView.as_view(),),
    path("login/", LoginUserView.as_view(),),
    path("update_password/", UpdatePasswordView.as_view()),
    path("update_user_data/", UpdateUserDataView.as_view()),
    path("update_profile_images/", UpdateUserProfileImageView.as_view(), ),
    path("get_users/", GetUsersListView.as_view(), ),
    path("increase_user_view_count/", IncreaseUserViewsCountView.as_view(),),
    path("single_user_id/<id>/", GetUserWithID.as_view()),

]
