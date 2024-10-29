from rest_framework.fields import SerializerMethodField

from shared.restframework.serizlaizers import DynamicFieldsModelSerializer
from shops.models import Product
from shops.serializers.shop import AttachmentModelSerializer


class ProductModelSerializer(DynamicFieldsModelSerializer):
    position = SerializerMethodField(read_only=True)
    attachments = AttachmentModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'full_price', 'purchase_price', 'unit', 'stock_status', 'position',
                  'attachments')  # Todo Proudctlarni qilish

    def get_position(self, obj):
        return obj.category.position if obj.category else None
