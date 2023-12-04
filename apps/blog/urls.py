from rest_framework import routers
from .views import BlogViewSet

render_router = routers.DefaultRouter()
render_router.register(r'blog', BlogViewSet, basename='blog')

urlpatterns = render_router.urls
