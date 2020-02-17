from rest_framework import serializers
from core.models import Item

class ItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'price',
            'description_item',
            'discount_price',
            'category',
            'label',
            'slug',
        ]