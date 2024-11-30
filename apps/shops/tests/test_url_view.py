import pytest
from django.urls import reverse_lazy


@pytest.mark.django_db
class TestShopUrl:
    def test_shop_url(self):
        currency_url = reverse_lazy('shops:shop-currency-list')
        assert currency_url == '/api/v1/shop/currency'

        language_url = reverse_lazy('shops:shop-language-list')
        assert language_url == '/api/v1/shop/language'

        shop_country_url = reverse_lazy('shops:shop-country-list')
        assert shop_country_url == '/api/v1/shop/shop-country'

        shop_category_url = reverse_lazy('shops:shop-category-list')
        assert shop_category_url == '/api/v1/shop/shop-category'

        shop_list_url = reverse_lazy('shops:shop-list')
        assert shop_list_url == '/api/v1/shop/shop'

        shop_detail_url = reverse_lazy('shops:shop-detail', kwargs={'pk': 1})
        assert shop_detail_url == '/api/v1/shop/shop/1'

        shop_categories_url = reverse_lazy('shops:shop-categories', kwargs={'shop_id': 1})
        assert shop_categories_url == '/api/v1/shop/shop/1/categories'

        shop_category_update_url = reverse_lazy('shops:shop-category-update', kwargs={'pk': 1})
        assert shop_category_update_url == '/api/v1/shop/shop/1/category'

        # shop_s3_file_update_url = reverse_lazy('shops:shop-s3-file-update')
        # assert shop_s3_file_update_url == '/api/v1/shop/shop/s3-file-update'
