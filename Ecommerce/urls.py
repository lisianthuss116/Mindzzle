from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from account.views import (register, profile, login)
from Ecommerce.api_routers import router
from django.contrib.auth import views as auth_view
from rest_framework.authtoken import views
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    # core
    path('', include('core.urls', namespace='core')),

    # register
    path('register/', register, name='register'),
    # accounts
    path('profile/', profile, name='profile'),
    # login
    path('login/', login, name='login'),
    # logout
    path('logout/', auth_view.LogoutView.as_view(
        template_name='auth/logout.html'), name='logout'),
    # api
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
