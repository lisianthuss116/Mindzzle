from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile),
]