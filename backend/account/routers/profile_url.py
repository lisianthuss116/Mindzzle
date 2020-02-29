from django.urls import path
from django.conf.urls import url
from account import views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import path, include

from account.views.profile import profile
import re

app_name = 'account'

urlpatterns = [
    path('<str:username>/', profile, name='profile'),
]