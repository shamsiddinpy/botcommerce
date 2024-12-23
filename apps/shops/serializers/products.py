from rest_framework.fields import SerializerMethodField, FileField, ListField
from rest_framework.serializers import Serializer

from shops.models import Product
from shops.serializers.shop import AttachmentModelSerializer


class ProductModelSerializer(Serializer):
    position = SerializerMethodField(read_only=True)
    attachments = AttachmentModelSerializer(many=True, read_only=True)
    file = ListField(child=FileField(write_only=True, required=False))

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'full_price', 'purchase_price', 'unit', 'stock_status', 'position',
                  'attachments', 'file', 'ikpu_code', 'packing_code', 'vat_percent', 'barcode', 'length', 'width',
                  'weight', 'height', 'length_class', 'weight_class', 'internal_notes', '')  # Todo Proudctlarni qilish
        read_only_fields = ('file',)

    def get_position(self, obj):
        return obj.category.position if obj.category else None
