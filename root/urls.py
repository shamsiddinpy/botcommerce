from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from root.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL

urlpatterns = ([
                   path('admin/', admin.site.urls),
                   path('api/v1/', include('apps.urls')),
                   path('api-auth', include('rest_framework.urls')),
               ] + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL, document_root=STATIC_ROOT))
