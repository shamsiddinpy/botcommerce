from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from shared.restframework.paginations import PageSortNumberPagination
from shops.models import (Category, Attachment)
from shops.serializers.category import (CategoryModelSerializer)


@extend_schema(tags=['Category'])
class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = PageSortNumberPagination
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Category.objects.filter(shop_id=shop_id)

    @extend_schema(
        request={
            'application/json': CategoryModelSerializer,
            'multipart/form-data': CategoryModelSerializer,  # For file uploads
        },
        responses={201: CategoryModelSerializer},
    )
    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')  # Multiple files can be uploaded
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        attachment = []
        for file in files:
            key = f"shop/ecommerce/category/images/{category.id}/{file.name}"
            url = f"https://fra1.digitaloceanspaces.com/botcommerce/{key}"
            Attachment.objects.create(
                content_type=ContentType.objects.get_for_model(Category),
                record_id=category.id,
                key=key,
                url=url,
            )
            attachment.append({
                'file_name': file.name,
                'url': url
            })
        response_data = serializer.data
        response_data['attachments'] = attachment  # Add file information to the response
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, HTTP_201_CREATED, headers=headers)
