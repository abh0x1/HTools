from django.urls import path
from . import views

app_name = 'pass_strength_checker'

urlpatterns = [
    path('', views.check_strength, name='pass_strength_checker'),
]
