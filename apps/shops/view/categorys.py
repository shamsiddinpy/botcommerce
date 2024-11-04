from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)

from shared.restframework.paginations import PageSortNumberPagination
from shops.models import (Category)
from shops.serializers.category import (CategoryModelSerializer)


@extend_schema(tags=['Category'])
class CategoryCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = PageSortNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Category.objects.filter(shop_id=shop_id)


@extend_schema(tags=['Category'])
class CategoryUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    pagination_class = PageSortNumberPagination

    # def category_visibility(request):
    #     category_id = request.data.get('category_id')
    #     show_in_ecommerce = request.data.get('show_in_ecommerce')
    #     category = Category.objects.get(pk=category_id)
    #     category.show_in_ecommerce = show_in_ecommerce
    #     category.save()
    #     return Response({"success": True})
