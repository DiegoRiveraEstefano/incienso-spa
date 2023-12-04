from rest_framework import routers
from .views import CartViewSet

router = routers.DefaultRouter()
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
]

urlpatterns += router.urls
