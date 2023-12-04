from rest_framework import routers
from .views import OrderViewSet

router = routers.DefaultRouter()
router.register('order', OrderViewSet, basename='order')

urlpatterns = [
]

urlpatterns += router.urls
