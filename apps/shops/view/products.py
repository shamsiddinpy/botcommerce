from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from shared.restframework.paginations import PageSortNumberPagination
from shops.serializers.products import ProductModelSerializer


@extend_schema(tags=['Products'])
class ProductsViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    pagination_class = PageSortNumberPagination
