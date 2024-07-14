from django.urls import path

from payments.views import InitializePaymentIntentView, UpdateUserPlan


urlpatterns = [
    path("update_users_plan/", UpdateUserPlan.as_view()),
    path("create_intent/", InitializePaymentIntentView.as_view(),)
]
