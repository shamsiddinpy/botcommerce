from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from shared.restframework.paginations import PageSortNumberPagination
from shops.models import Product
from shops.serializers.products import ProductModelSerializer


@extend_schema(tags=['Products'])
class ProductsListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductModelSerializer
    pagination_class = PageSortNumberPagination
    queryset = Product.objects.all()


