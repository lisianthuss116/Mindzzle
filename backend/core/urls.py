from django.urls import path
from .views import (Home, ProductDetail)

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='homes'),
    path('product/<slug>', ProductDetail.as_view(), name='product'),
    path('', Home.as_view(), name='homes'),
]
