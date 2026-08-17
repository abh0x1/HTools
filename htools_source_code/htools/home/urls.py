from django.urls import path
from .views import landing_page, dashboard

app_name = "home"

urlpatterns = [
    path("", landing_page, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
]
