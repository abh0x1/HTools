from django.urls import path
from . import views

app_name = "header_grabber"

urlpatterns = [
    path("", views.header_form, name="header_form"),
]
