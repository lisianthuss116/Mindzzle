from rest_framework import routers
from backend.api.viewsets import item_viewset

router = routers.DefaultRouter()
router.register(r'items', item_viewset.ItemView, basename='items')
