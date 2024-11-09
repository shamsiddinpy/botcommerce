from django.contrib.contenttypes.models import ContentType
from rest_framework.fields import FileField
from rest_framework.serializers import Serializer

from shared.restframework.serizlaizers import DynamicFieldsModelSerializer
from shops.models import (Category, Attachment)
from shops.serializers.shop import AttachmentModelSerializer


class FileUploadSerializer(Serializer):
    file = FileField()


class CategoryModelSerializer(DynamicFieldsModelSerializer):  # Todo Categoryani ko'rish
    attachments = AttachmentModelSerializer(many=True, read_only=True)
    file = FileUploadSerializer(many=True, required=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'emoji', 'parent', 'show_in_ecommerce', 'status', 'description', 'position',
                  'shop', 'attachments', 'file')
        read_only_fields = ('show_in_ecommerce', 'status', 'shop', 'id', 'file')

    def create(self, validated_data):
        attachment_data = validated_data.pop('attachments', [])
        validated_data['status'] = Category.Status.ACTIVE
        shop_id = self.context['view'].kwargs['shop_id']
        category = Category.objects.create(shop_id=shop_id, **validated_data)
        files = self.context.get('request').FILES.getlist('file')
        for file in files:
            key = f"shop/ecommerce/category/images/{category.id}/{file.name}"
            url = f"https://fra1.digitaloceanspaces.com/botcommerce/{key}"
            Attachment.objects.create(
                content_type=ContentType.objects.get_for_model(Category),
                record_id=category.id,
                key=key,
                url=url,

            )
        return category

    def get_parent(self, instance):
        if instance.parent_id:
            return {"name": instance.parent.name}
        return {'name': ''}

    def to_representation(self, instance: Category):
        cate = super().to_representation(instance)
        cate['id'] = instance.id
        cate['show_in_ecommerce'] = instance.show_in_ecommerce
        cate['parent'] = self.get_parent(instance)
        return cate
