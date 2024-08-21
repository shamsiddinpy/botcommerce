from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('user/', include('users.urls')),
    path('shop/', include('shops.urls')),
    path('order/', include('orders.urls')),
    path('teligram/', include('telegram.urls')),
]
