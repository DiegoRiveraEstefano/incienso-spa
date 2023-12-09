from rest_framework import routers
from .views import BlogViewSet, BlogApiViewSet

render_router = routers.DefaultRouter()
render_router.register(r'blog', BlogViewSet, basename='blog')
render_router.register('api/blog', BlogApiViewSet, basename='blog-api')

urlpatterns = render_router.urls
