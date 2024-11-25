from django.contrib.contenttypes.models import ContentType
from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from shared.restframework.paginations import PageSortNumberPagination
from shops.models import (Category, Attachment)
from shops.serializers.category import (CategoryModelSerializer)


@extend_schema(tags=['Category'])  # category qo'shadigan API
class CategoryCreateAPIView(ListCreateAPIView, ):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = PageSortNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Category.objects.filter(shop_id=shop_id)


@extend_schema(tags=['Category'])  # Attachemn categoryni rasmini o'zini o'chrish
class CategoryAttachmentDeleteAPIView(APIView):

    def delete(self, request, category_id, attachment_id):
        category = get_object_or_404(Category, id=category_id)
        content_type = ContentType.objects.get_for_model(Category)
        attachment = get_object_or_404(
            Attachment,
            content_type=content_type,
            record_id=category.id,
            id=attachment_id,
        )
        try:
            if attachment.file:
                attachment.file.delete(save=False)
        except Exception as e:
            return Response({"error": f"Error deleting file: {str(e)}"}, HTTP_500_INTERNAL_SERVER_ERROR)
        attachment.delete()
        return Response({"detail": "Attachment successfully deleted."}, HTTP_204_NO_CONTENT)


@extend_schema(tags=['Category'])  # Rasimni yuklab olish (categoriyadagi rasimni yuklab olish kerak
class DownloadCategoryImageAPIView(APIView):

    def get(self, request, image_id):  # Todo buni ko'rish kerak rasimni yuklab olmaydpi
        try:
            attachment = Attachment.objects.get(id=image_id)
            file_response = FileResponse(attachment.file.open(), content_type=attachment.content_type)
            file_response['Content-Disposition'] = f'attachment; filename="{attachment.file.name.split("/")[-1]}"'
            return file_response
        except Attachment.DoesNotExist:
            return Response({"error": "Image not found.."}, HTTP_404_NOT_FOUND)
