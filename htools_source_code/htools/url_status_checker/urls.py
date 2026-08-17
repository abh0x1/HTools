from django.urls import path
from .views import index, check_status

app_name = "url_status_checker"

urlpatterns = [
    path("", index, name="url_index"),
    path("check_status/", check_status, name="check_status"),
]
