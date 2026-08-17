from django.urls import path
from . import views

app_name = 'base64_tool'

urlpatterns = [
    path('', views.base64_encoder_decoder, name='base64_tool'),
]
