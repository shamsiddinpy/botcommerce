from django.urls import path

from telegram.views import TokenCreateAPIView

urlpatterns = [
    path('shop', TokenCreateAPIView.as_view(), name='token_create'),
    # path('orders', include('apps.orders.urls')),
    # path('shop', include('apps.view.urls')),
    # path('telegram', include('apps.telegram.urls')),
]
