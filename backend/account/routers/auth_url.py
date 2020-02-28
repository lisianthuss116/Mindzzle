from django.urls import path
from django.conf.urls import url
from account import views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import path, include

from account.views import auth

app_name = 'auth'

urlpatterns = [
    # register
    path('register/', auth.RegisterView.as_view(), name='register'),
    # login
    path('login/', auth.login, name='login'),
]
