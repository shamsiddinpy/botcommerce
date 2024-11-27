from django.contrib.contenttypes.models import ContentType
from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404, ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from shared.restframework.paginations import PageSortNumberPagination
from shops.models import (Category, Attachment, Shop)
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


@extend_schema(tags=['Category'])
class CategoryDestroyAPIView(DestroyAPIView):
    serializer_class = CategoryModelSerializer

    def get_queryset(self):
        """
        Foydalanuvchining do'koniga tegishli kategoriyalarni filtrlaydi.
        """
        shop_id = self.kwargs.get('shop_id')
        return Category.objects.filter(shop_id=shop_id)

    def perform_destroy(self, instance):
        """
         Kategoriyani o'chirishdan oldin tekshiradi, faqat o'ziga tegishli shop'ga tegishli bo'lsa o'chiradi.
        """
        shop_id = self.kwargs.get('shop_id')
        if instance.shop_id != shop_id:
            raise PermissionDenied("You can only delete a category in your own store.")
        return super().perform_destroy(instance)


@extend_schema(tags=['Category'])
class CategoryPositionUpdateAPIView(APIView):
    def patch(self, request, pk, shop_id, *args, **kwargs):
        try:
            shop = get_object_or_404(Shop, pk=shop_id)
            category = Category.objects.get(pk=pk, shop=shop)
            new_position = request.data.get('position')
            if new_position is None:
                raise ValidationError({'error': 'Position is required'})
            Category.update_position(category.id, new_position)
            return Response({'status': 'Position updated'}, status=200)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        except ValidationError as e:
            return Response(e.detail, status=400)


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


@extend_schema(tags=['Category'])  # Categoryni yanglish
class UpdateCategoryImageAPIView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = PageSortNumberPagination

    def partial_update(self, request, *args, **kwargs):
        category = self.get_object()
        file = request.FILES.get('file', None)
        if file:
            attachment, created = Attachment.objects.get_or_create(
                content_type=ContentType.objects.get_for_model(Category),
                record_id=category.id,
                defaults={'file': file}
            )
            if not created:
                attachment.file = file
                attachment.save()
        return super().partial_update(request, *args, **kwargs)

# @extend_schema(tags=['Category'])
# class ExportCategoryCSVAPIView(APIView):  # Categoryni
#     def get(self, request, shop_id):
#         categories = Category.objects.filter(id=shop_id)
#         shop_categories = ShopCategory.objects.all()
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="category_uz.csv"'
#         writer = csv.writer(response)
#         writer.writerow(['type', 'name', 'parent', 'description'])
#         for category in categories:
#             writer.writerow(
#                 ['Category', category.name, category.parent if category.parent else '', category.description])
#
#         for shop_category in shop_categories:
#             writer.writerow(
#                 [
#                     'Shop Category',
#                     shop_category.name,
#                 ]
#             )
#         return response
#
#
# @extend_schema(tags=['Category'])
# class CategoryShopCategoryImportAPIView(APIView):
#     def post(self, request, shop_id):
#         # Shopni tekshirish
#         shop = Shop.objects.filter(id=shop_id, owner=request.user).first()
#         if not shop:
#             return Response({"error": "Shop not found or you do not have permission to access this shop."},
#                             status=HTTP_403_FORBIDDEN)
#
#         import_file = request.FILES.get('import_file', None)
#         if not import_file or not import_file.name.endswith('.csv'):
#             return Response({"error": "Please upload a valid CSV file!"}, status=HTTP_400_BAD_REQUEST)
#
#         try:
#             decoded_file = import_file.read().decode('utf-8').splitlines()
#             reader = csv.DictReader(decoded_file)
#
#             for row in reader:
#                 # ShopCategoryni yaratish yoki olish
#                 shop_category = None
#                 if 'shop_category_name' in row and row['shop_category_name']:
#                     shop_category, _ = ShopCategory.objects.get_or_create(name=row['shop_category_name'])
#
#                 # Parentni topish
#                 parent = None
#                 if 'parent' in row and row['parent']:
#                     parent = Category.objects.filter(name=row['parent'], shop=shop).first()
#                     if not parent:
#                         return Response({"error": f"No main category found in this shop: {row['parent']}"},
#                                         status=HTTP_404_NOT_FOUND)
#
#                 # Category yaratish
#                 if 'name' in row and row['name']:
#                     Category.objects.create(
#                         name=row['name'],
#                         description=row.get('description', ''),
#                         parent=parent,
#                         shop=shop,  # Faqat berilgan shop uchun
#                         position=row.get('position', 1),
#                         status=row.get('status', Category.Status.INACTIVE),
#                         show_in_ecommerce=row.get('show_in_ecommerce', 'false').lower() == 'true'
#                     )
#                 else:
#                     return Response({"error": "Category 'name' field is required in CSV!"}, status=HTTP_400_BAD_REQUEST)
#
#             return Response({"detail": "Data imported from CSV file successfully."}, status=HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": f"An error occurred: {str(e)}"}, status=HTTP_400_BAD_REQUEST)
