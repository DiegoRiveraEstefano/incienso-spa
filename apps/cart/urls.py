from rest_framework import routers
from .views import CartViewSet, CartApiViewSet

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'api/cart', CartApiViewSet, basename='cart-api')

urlpatterns = router.urls
