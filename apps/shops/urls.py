from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from shops.views import (CountryListAPIView, CurrencyListAPIView,
                         LanguageListAPIView, ShopCategoryListAPIView,
                         ShopModelViewSet, CategoryCreateAPIView, CategoryUpdateAPIView)

app_name = 'shop'
router = SimpleRouter(False)
router.register(r'shop', ShopModelViewSet, basename='shop')
# router.register(r'category', CategoryCreateAPIView, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('currency', CurrencyListAPIView.as_view(), name='shop-currency-list'),
    path('language', LanguageListAPIView.as_view(), name='shop-language-list'),
    path('shop-country', CountryListAPIView.as_view(), name='shop-country-list'),
    path('shop-category', ShopCategoryListAPIView.as_view(), name='shop-category-list'),
    path('shop/<int:shop_id>/category', CategoryCreateAPIView.as_view(), name='shop-category-list'),
    path('shop/category/<int:pk>', CategoryUpdateAPIView.as_view(), name='shop-category-update'),
]
