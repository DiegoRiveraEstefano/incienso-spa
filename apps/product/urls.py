from rest_framework import routers
from .views import ProductViewSet, ProductDiscountApiViewSet, ProductApiViewSet

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'api/product/api', ProductApiViewSet, basename='product-api')
router.register(r'api/product/discounts', ProductDiscountApiViewSet, basename='product-discount-api')

urlpatterns = router.urls
