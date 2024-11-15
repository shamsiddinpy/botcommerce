from django.contrib.contenttypes.models import ContentType
from rest_framework.fields import FileField

from shared.restframework.serizlaizers import DynamicFieldsModelSerializer
from shops.models import (Category, Attachment)
from shops.serializers.shop import AttachmentModelSerializer


class CategoryModelSerializer(DynamicFieldsModelSerializer):  # Todo Categoryani ko'rish
    attachments = AttachmentModelSerializer(many=True, read_only=True)
    file = FileField(write_only=True, required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'emoji', 'parent', 'show_in_ecommerce', 'status', 'description', 'position',
                  'shop', 'attachments', 'file')
        read_only_fields = ('show_in_ecommerce', 'status', 'shop', 'id', 'file')

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        validated_data['status'] = Category.Status.ACTIVE
        shop_id = self.context['view'].kwargs['shop_id']
        category = Category.objects.create(shop_id=shop_id, **validated_data)
        if file:
            Attachment.objects.create(content_type=ContentType.objects.get_for_model(Category),
                                      record_id=category.id, file=file)
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
