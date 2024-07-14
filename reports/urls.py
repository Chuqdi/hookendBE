from django.urls import path

from reports.views import ReportUserView


urlpatterns = [
    path("report_user/", ReportUserView.as_view(), name="report_user"),
]
