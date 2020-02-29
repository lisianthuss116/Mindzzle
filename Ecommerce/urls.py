from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import path, include

from rest_framework.authtoken import views

from account.views import auth
from Ecommerce.api_routers import router
auth_url = 'account.routers.auth_url'
profile_url = 'account.routers.profile_url'



urlpatterns = [
    path('admin/', admin.site.urls),
    # core
    path('', include('core.urls', namespace='core')),
    # auth
    path('auth/', include(auth_url, namespace='auth')),
    # account
    path('account/', include(profile_url, namespace='account')),
    # logout
    path('logout/', auth_view.LogoutView.as_view(
        template_name='auth/logout.html'), name='logout'),
    # api
    path('api/v1/', include(router.urls)),
    path('api/v2/', include('api.urls', namespace='api')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

    # confim-email
    path('confirm-email/<str:user_id>/<str:token>',
         auth.ConfirmRegisterView.as_view(), name='confirm-email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
