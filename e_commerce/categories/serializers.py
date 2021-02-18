from rest_framework import serializers
from .models import *


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategoriesSerializer(serializers.ModelSerializer):
    subcategories = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ('id', 'category_name', 'status', 'category_image', 'alt', 'parent', 'category_description', 'slug', 'meta_title', 'meta_description',
                  'meta_keyword', 'created_at', 'updated_at', 'subcategories')
