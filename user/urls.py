from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'user'


urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(), name='login'),
]