from django.urls import include, path
from rest_framework.routers import SimpleRouter

from shops.view.categorys import CategoryCreateAPIView, CategoryAttachmentDeleteAPIView, DownloadCategoryImageAPIView
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

    path('category/<int:category_id>/shop-file-upload', CategoryAttachmentDeleteAPIView.as_view(),
         name='shop-category-attachment-delete'),
    path('category/<int:category_id>/shop-file-upload/<int:attachment_id>', DownloadCategoryImageAPIView.as_view(),
         name='shop-category-attachment-download'),
    path('', include(router.urls)),

]
