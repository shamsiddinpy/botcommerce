from celery.bin.control import status
from django.contrib.contenttypes.models import ContentType
from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from shared.restframework.paginations import PageSortNumberPagination
from shops.models import (Category, Attachment)
from shops.serializers.category import (CategoryModelSerializer)


@extend_schema(tags=['Category'])  # category qo'shadigan API
class CategoryCreateAPIView(CreateAPIView):
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
        try:
            category = Category.objects.get(id=category_id)
            attachment = Attachment.objects.get(
                content_type=ContentType.objects.get_for_model(Category),
                record_id=category.id,
                id=attachment_id
            )
            # Faylni o'chirish
            attachment.file.delete(save=False)  # Fayl tizimdan o'chadi
            attachment.delete()  # Ma'lumotlar bazasidan o'chadi

            return Response({"detail": "Attachment successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        except Attachment.DoesNotExist:
            return Response({"error": "Attachment not found."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Category'])  # Rasimni yuklab olish (categoriyadagi rasimni yuklab olish kerak
class DownloadCategoryImageAPIView(APIView):

    def get(self, request, image_id):  # Todo buni ko'rish kerak rasimni yuklab olmaydpi
        try:
            attachment = Attachment.objects.get(id=image_id)
            file_response = FileResponse(attachment.file.open(), content_type=attachment.content_type)
            file_response['Content-Disposition'] = f'attachment; filename="{attachment.file.name.split("/")[-1]}"'
            return FileResponse(file_response)
        except Attachment.DoesNotExist:
            return Response({"error": "Image not found.."}, status=status.HTTP_404_NOT_FOUND)
