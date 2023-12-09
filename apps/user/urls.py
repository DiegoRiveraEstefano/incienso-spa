from rest_framework import routers
from .views import UserViewSet, UserApiViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('api/user', UserApiViewSet, basename='user-api')

urlpatterns = [
]

urlpatterns += router.urls