from django.urls import include, path
from rest_framework.routers import SimpleRouter

from shops.view.categorys import CategoryCreateAPIView, CategoryUpdateAPIView, CategoryImportAPIView
from shops.view.products import ProductsViewSet
from shops.view.shops import ShopModelViewSet, CurrencyListAPIView, LanguageListAPIView, CountryListAPIView, \
    ShopCategoryListAPIView

app_name = 'shops'
router = SimpleRouter(False)
router.register(r'shop', ShopModelViewSet, basename='shop')
router.register(r'product', ProductsViewSet, basename='product')

urlpatterns = [
    path('currency', CurrencyListAPIView.as_view(), name='shop-currency-list'),
    path('language', LanguageListAPIView.as_view(), name='shop-language-list'),
    path('shop-country', CountryListAPIView.as_view(), name='shop-country-list'),
    path('shop-category', ShopCategoryListAPIView.as_view(), name='shop-category-list'),
    path('shop/<int:shop_id>/categories', CategoryCreateAPIView.as_view(), name='shop-categories'),
    path('shop/categories/<int:pk>', CategoryUpdateAPIView.as_view(), name='shop-category-update'),
    path('shop/s3-file-update', CategoryImportAPIView.as_view(), name='shop-s3-file-update'),
    path('', include(router.urls)),

]
