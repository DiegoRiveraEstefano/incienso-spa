from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from django.contrib.auth import logout
from django.conf.urls import include

from apps.user.exceptions import permission_denied_view
from .views import Index


urlpatterns = [
    path('', Index.as_view()),
    path('admin/', admin.site.urls, name='admin'),
    path('logout/', logout, {'next_page': '/'}, name='logout'),
    path('', include('apps.user.urls')),
    path('', include('apps.product.urls')),
    path('', include('apps.blog.urls')),
    path('', include('apps.cart.urls')),
    path('', include('apps.order.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)