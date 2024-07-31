from django.urls import include, path
from rest_framework.routers import DefaultRouter
from shops.views import (CountryListAPIView, CurrencyListAPIView,
                         LanguageListAPIView, ShopCategoryListAPIView,
                         ShopCreateAPIView)

router = DefaultRouter()
router.register(r'shop', ShopCreateAPIView, basename='shop')
urlpatterns = [
    path('', include(router.urls)),
    # path('shops/', ShopCreateAPIView.as_view(), name='shop-list'),
    path('currency', CurrencyListAPIView.as_view(), name='shop-currency-list'),
    path('language', LanguageListAPIView.as_view(), name='shop-language-list'),
    path('shop-country', CountryListAPIView.as_view(), name='shop-country-list'),
    path('shop-category', ShopCategoryListAPIView.as_view(), name='shop-category-list'),
    # path('category', CategoryListAPIView.as_view(), name='shop-category-list'),
]
