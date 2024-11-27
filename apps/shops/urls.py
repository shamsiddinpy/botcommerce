from django.urls import include, path
from rest_framework.routers import SimpleRouter

from shops.view.categorys import CategoryCreateAPIView, CategoryAttachmentDeleteAPIView, DownloadCategoryImageAPIView, \
    UpdateCategoryImageAPIView, CategoryDestroyAPIView, CategoryPositionUpdateAPIView
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

    path('category/<int:category_id>/shop-file-upload/<int:attachment_id>', CategoryAttachmentDeleteAPIView.as_view(),
         name='shop-category-attachment-delete'),
    path('category/<int:image_id>/shop-file-upload', DownloadCategoryImageAPIView.as_view(),
         name='shop-category-attachment-download'),
    path('shop/<int:pk>category', UpdateCategoryImageAPIView.as_view(), name='shop-category-update'),
    path('shop/<int:shop_id>/category/<int:pk>', CategoryDestroyAPIView.as_view(), name='shop-category-destroy'),
    path('shop/<int:shop_id>/category-position/<int:pk>', CategoryPositionUpdateAPIView.as_view(), name='shop-category-position'),
    # path('shop/<int:shop_id>/export', ExportCategoryCSVAPIView.as_view(), name='shop-category-attachment-export'),
    # Categorylarni export qiladigan API
    # path('shop/<int:shop_id>/import/category', CategoryShopCategoryImportAPIView.as_view(),
    #      name='shop-category-attachment-import'),  # Categorylari import qiladigan API

    path('', include(router.urls)),

]
