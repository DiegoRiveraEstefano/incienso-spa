from rest_framework import routers
from .views import OrderViewSet, OrderApiViewSet

router = routers.DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('api/order', OrderApiViewSet, basename='order-api')

urlpatterns = [
]

urlpatterns += router.urls
