# ip_information/urls.py
from django.urls import path
from .views import ip_info

app_name = 'ip_information'

urlpatterns = [
    path('', ip_info, name='index'),
]
