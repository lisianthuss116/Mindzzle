from django.urls import path
from .views import (Home, ProductDetail, add_to_cart, remove_from_cart)

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='homes'),
    path('product/<slug>', ProductDetail.as_view(), name='product'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
]
