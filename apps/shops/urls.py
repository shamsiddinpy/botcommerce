from django.urls import include, path
from rest_framework.routers import SimpleRouter

from shops.views import (CategoryCreateAPIView, CategoryUpdateAPIView,
                         CountryListAPIView, CurrencyListAPIView,
                         LanguageListAPIView, ShopCategoryListAPIView,
                         ShopModelViewSet)

app_name = 'shops'
router = SimpleRouter(False)
router.register(r'shop', ShopModelViewSet, basename='shop')
# router.register(r'category', CategoryCreateAPIView, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('currency', CurrencyListAPIView.as_view(), name='shop-currency-list'),
    path('language', LanguageListAPIView.as_view(), name='shop-language-list'),
    path('shop-country', CountryListAPIView.as_view(), name='shop-country-list'),
    path('shop-categories', ShopCategoryListAPIView.as_view(), name='shop-categories-list'),
    path('shop/<int:shop_id>/categories', CategoryCreateAPIView.as_view(), name='shop-categories'),
    path('shop/categories/<int:pk>', CategoryUpdateAPIView.as_view(), name='shop-category-update'),
]
