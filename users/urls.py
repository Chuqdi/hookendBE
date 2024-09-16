from django.urls import path
from .views import ActivateUserAccount, GetUserWithID, ImplementAdavancedFilterView, IncreaseUserViewsCountView, Me, RegisterUserView, SendUserActivationEmail, UpdatePasswordView, UpdateUserDataView, LoginUserView, UpdateUserProfileImageView, GetUsersListView,GetUserMatchView,UpdateUserAdvancedFilterFieldView,RemoveAdvancedFilterField, UpdatePassworAuthdView,UpdateLocationView,DeleteAccountView, GetUserWithPhoneNumber,UpdateUserCurrentLocation


urlpatterns = [
    path("me/", Me.as_view(), name="me"),
    path("register/", RegisterUserView.as_view(),),
    path("login/", LoginUserView.as_view(),),
    path("update_password/", UpdatePasswordView.as_view()),
    path("update_user_data/", UpdateUserDataView.as_view()),
    path("update_user_advanced_filter_data/", UpdateUserAdvancedFilterFieldView.as_view(),),
    path("delete_account/", DeleteAccountView.as_view()),
    path("update_profile_images/", UpdateUserProfileImageView.as_view(), ),
    path("update_user_current_location/", UpdateUserCurrentLocation.as_view(),),
    path("activate_account/", SendUserActivationEmail.as_view(), ),
    path("activate_email_account/", ActivateUserAccount.as_view(), ),
    path("get_users/", GetUsersListView.as_view(), ),
    path("update_location/",UpdateLocationView.as_view(),),
    path("update_password_auth/",UpdatePassworAuthdView.as_view(),),
    path("get_user_matches/",GetUserMatchView.as_view(), ),
    path("remove_advanced_filter/", RemoveAdvancedFilterField.as_view(),),
    path("implement_advanced_filter/<email>/",ImplementAdavancedFilterView.as_view()),
    path("increase_user_view_count/", IncreaseUserViewsCountView.as_view(),),
    path("single_user_id/<id>/", GetUserWithID.as_view()),
    path("single_user_phone_number/<phone_number>/", GetUserWithPhoneNumber.as_view()),

]
