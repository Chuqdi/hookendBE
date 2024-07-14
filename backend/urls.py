
from django.contrib import admin
from django.urls import path, include




ROOT_URL="api/v1/"
urlpatterns = [
    path('admin/', admin.site.urls),

    path(ROOT_URL +"users/", include("users.urls")),
    path(ROOT_URL +"likes/", include("likes.urls")),
    path(ROOT_URL +"payments/", include("payments.urls")),
    path(ROOT_URL +"blocks/", include("blocks.urls")),
    path(ROOT_URL +"reports/", include("reports.urls")),

]
