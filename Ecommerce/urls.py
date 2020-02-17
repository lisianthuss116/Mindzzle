from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from account.views import register
from Ecommerce.api_routers import router
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # core
    path('', include('core.urls', namespace='core')),

    # register
    path('register/', register, name='register'),
    # login
    path('login/', auth_view.LoginView.as_view(
        template_name='auth/login.html'), name='login'),
    # logout
    path('logout/', auth_view.LogoutView.as_view(
        template_name='auth/logout.html'), name='logout'),
    # api
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
