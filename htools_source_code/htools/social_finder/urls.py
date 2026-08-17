from django.urls import path
from . import views

app_name = 'social_finder'

urlpatterns = [
    path('', views.social_finder, name='social_finder'),
]