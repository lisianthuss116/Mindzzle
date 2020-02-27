from django.urls import path
from django.conf.urls import url

from api.viewsets import item_viewset

app_name = 'api'

urlpatterns = [
    path('items/', item_viewset.item_view, name='items'),
    path('items/<int:pk>', item_viewset.item_detail, name='items-detail')
]