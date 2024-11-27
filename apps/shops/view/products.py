from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from shared.restframework.paginations import PageSortNumberPagination
from shops.models import Product
from shops.serializers.products import ProductModelSerializer


@extend_schema(tags=['Products'])
class ProductsListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductModelSerializer
    pagination_class = PageSortNumberPagination

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Product.objects.filter(shop_id=shop_id)

    def get_serializer(self, *args, **kwargs):
        field = self.request.query_params.get('field')
        if field:
            fields = field.split(',')
        else:
            fields = ['name', 'description', 'category', 'full_price', 'purchase_price', 'unit', 'stock_status',
                      'position', 'attachments']
        return super().get_serializer(*args, fields=fields, **kwargs)
