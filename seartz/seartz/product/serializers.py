from rest_framework import serializers
from .models import *


class ProductGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGalleryImage
        fields = "__all__"


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = "__all__"


class ProductCanvasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCanvas
        fields = "__all__"


class ProductHeartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHeart
        fields = "__all__"


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = "__all__"


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    product_gallery_image = ProductGalleryImageSerializer(read_only=True)
    product_size = ProductSizeSerializer(read_only=True)
    product_canvas = ProductCanvasSerializer(read_only=True)
    product_heart = ProductHeartSerializer(read_only=True)
    product_comment = ProductCommentSerializer(read_only=True)
    product_review = ProductReviewSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'product_code', 'user_id', 'category_id', 'product_name', 'product_description', 'product_home_image', 'product_specification',
                  'certificate_by', 'certificate_file', 'price', 'selling_price', 'price_off', 'status', 'likes', 'view', 'heart', 'total_comment',
                  'total_review', 'is_feature', 'is_approved', 'approved_by', 'slug', 'meta_description', 'meta_keyword', 'meta_title', 'available_stock',
                  'delivery_charge', 'is_cod', 'delivery_time', 'created_at', 'updated_at', 'product_gallery_image', 'product_size', 'product_canvas',
                  'product_heart', 'product_comment', 'product_review')
