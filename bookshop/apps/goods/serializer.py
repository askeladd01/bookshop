from django.db.models import Q
from rest_framework import serializers

from . import models


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ['name', 'link', 'image']


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品二级类别序列化
    """

    class Meta:
        model = models.GoodsCategory
        fields = ['id', 'code', 'name', 'parent_category', 'is_tab']


class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = models.GoodsCategory
        fields = ['id', 'code', 'name', 'sub_cat', 'is_tab']


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsImage
        fields = ['image']


class GoodsDetailSerializer(serializers.ModelSerializer):
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = models.Goods
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goods
        fields = ['id', 'name', 'goods_front_image', 'market_price', 'shop_price']


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotSearchWords
        fields = ['keywords']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsCategoryBrand
        fields = ['id', 'name', 'image', 'category']


class IndexCategorySerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = models.IndexAd
        fields = ['category', 'goods']
