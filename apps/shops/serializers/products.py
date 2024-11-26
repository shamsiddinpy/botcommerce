from rest_framework.fields import SerializerMethodField, FileField

from shared.restframework.serizlaizers import DynamicFieldsModelSerializer
from shops.models import Product
from shops.serializers.shop import AttachmentModelSerializer


class ProductModelSerializer(DynamicFieldsModelSerializer):
    position = SerializerMethodField(read_only=True)
    attachments = AttachmentModelSerializer(many=True, read_only=True)
    file = FileField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'full_price', 'purchase_price', 'unit', 'stock_status', 'position',
                  'attachments', 'file')  # Todo Proudctlarni qilish
        read_only_fields = ('file',)

    def get_position(self, obj):
        return obj.category.position if obj.category else None
