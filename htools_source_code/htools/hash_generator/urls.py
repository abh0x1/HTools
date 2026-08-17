from django.urls import path
from . import views

app_name = 'hash_generator'

urlpatterns = [
    path('', views.generate_hash, name='hash_generator'),
]
