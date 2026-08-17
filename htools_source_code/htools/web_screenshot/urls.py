from django.urls import path
from .views import site_checker

app_name = "web_screenshot"

urlpatterns = [
    path("", site_checker, name="index"),
]
