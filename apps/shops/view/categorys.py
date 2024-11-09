from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView

from shared.restframework.paginations import PageSortNumberPagination
from shops.models import (Category)
from shops.serializers.category import (CategoryModelSerializer)


@extend_schema(tags=['Category'])
class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = PageSortNumberPagination
    # parser_classes = [MultiPartParser, FormParser]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Category.objects.filter(shop_id=shop_id)

    # def create(self, request, *args, **kwargs):
    #     files = request.FILES.getlist('file')  # Multiple files can be uploaded
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     category = serializer.save()
    #     for file in files:
    #         key = f"shop/ecommerce/category/images/{category.id}/{file.name}"
    #         url = f"https://fra1.digitaloceanspaces.com/botcommerce/{key}"
    #         Attachment.objects.create(
    #             content_type=ContentType.objects.get_for_model(Category),
    #             record_id=category.id,
    #             key=key,
    #             url=url,
    #         )
    #
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
