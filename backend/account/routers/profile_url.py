from django.urls import path
from django.conf.urls import url
from account import views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import path, include

from account.views import profile as profile_view
import re

app_name = 'profile'

urlpatterns = [
    path('profile/', profile_view.profile, name='profile'),
]