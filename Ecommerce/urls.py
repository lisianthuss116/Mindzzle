from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import path, include

from account.views import (
    RegisterView,
    ConfirmRegisterView,
    profile,
    login)
from Ecommerce.api_routers import router
import re

from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # core
    path('', include('core.urls', namespace='core')),
    # confim-email
    path('confirm-email/<str:user_id>/<str:token>',
         ConfirmRegisterView.as_view(), name='confirm-email'),

    # register
    path('register/', RegisterView.as_view(), name='register'),
    # accounts
    path('profile/', profile, name='profile'),
    # login
    path('login/', login, name='login'),
    # logout
    path('logout/', auth_view.LogoutView.as_view(
        template_name='auth/logout.html'), name='logout'),
    # api
    path('api/v1/', include(router.urls)),
    path('api/v2/', include('api.urls', namespace='api')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
