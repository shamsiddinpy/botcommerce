from rest_framework.fields import FileField
from rest_framework.serializers import Serializer

from shared.restframework.serizlaizers import DynamicFieldsModelSerializer
from shops.models import (Category)
from shops.serializers.shop import AttachmentModelSerializer


class FileUploadSerializer(Serializer):
    file = FileField()


class CategoryModelSerializer(DynamicFieldsModelSerializer):  # Todo Categoryani ko'rish
    attachments = AttachmentModelSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'emoji', 'parent', 'show_in_ecommerce', 'status', 'description', 'position',
                  'shop', 'attachments')
        read_only_fields = ('show_in_ecommerce', 'status', 'shop', 'id')

    def create(self, validated_data):
        shop_id = self.context['view'].kwargs['shop_id']
        category = Category.objects.create(shop_id=shop_id, **validated_data)
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
