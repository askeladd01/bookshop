import time
from random import Random

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from goods.serializer import GoodsSerializer
from goods.models import Goods
from . import models


class ShopCartDetailSerializer(serializers.ModelSerializer):
    # 一条购物车关系记录对应的只有一个goods。
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = models.ShoppingCart
        fields = ("goods", "nums")


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(label="数量", min_value=1, default=1, error_messages={"min_value": "商品数量不能小于一"})
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def validate(self, attrs):
        nums = attrs.get("nums")
        goods = attrs.get("goods")
        if goods.goods_num < nums:
            raise ValidationError('商品库存不足')
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = models.ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = models.ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = models.OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    pay_url = serializers.SerializerMethodField(read_only=True)
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = models.OrderInfo
        fields = "__all__"

    def get_pay_url(self, obj):
        from bookshop.libs.alipay import alipay, gateway
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            subject=obj.subject,
            return_url=settings.RETURN_URL,  # get回调，前台地址
            notify_url=settings.NOTIFY_URL  # post回调，后台地址
        )
        return gateway + order_string


class OrderSerializer(serializers.ModelSerializer):
    pay_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.OrderInfo
        fields = ['id', 'subject', 'order_sn', 'pay_type', 'pay_status', 'order_mount', "post_script", "address", "signer_name",
                  "singer_mobile", 'pay_url', 'create_time', ]
        extra_kwargs = {
            'pay_type': {'required': True},
            'order_mount': {'required': True},
        }

    def _check_price(self, attrs):
        """
        后台再次验证订单金额及商品库存
        """
        shop_carts = models.ShoppingCart.objects.filter(user=self.context['request'].user)
        order_mount = attrs.get('order_mount')
        check_price = 0
        goods_nums = {}
        for record in shop_carts:
            check_price += record.goods.shop_price * record.nums
            if record.goods.goods_num < record.nums:
                goods_nums[record.goods.name] = '商品库存不足'
        if goods_nums:
            raise ValidationError(goods_nums)
        if check_price != order_mount:
            raise ValidationError('价格不合法')

        return order_mount

    def _get_order_sn(self):
        # 当前时间+userid+随机数
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def get_pay_url(self, obj):
        from bookshop.libs.alipay import alipay, gateway
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            subject=obj.subject,
            return_url=settings.RETURN_URL,  # get回调，前台地址
            notify_url=settings.NOTIFY_URL  # post回调，后台地址
        )
        return gateway + order_string

    def _before_create(self, attrs, user, order_sn):
        attrs['user'] = user
        attrs['order_sn'] = order_sn

    def validate(self, attrs):
        order_mount = self._check_price(attrs)
        order_sn = self._get_order_sn()
        user = self.context["request"].user

        self._before_create(attrs, user, order_sn, )
        return attrs

    def create(self, validated_data):
        order = models.OrderInfo.objects.create(**validated_data)
        # 获取到用户购物车里的商品
        shop_carts = models.ShoppingCart.objects.filter(user=self.context["request"].user)
        for record in shop_carts:
            models.OrderGoods.objects.create(order=order, goods=record.goods, goods_num=record.nums,
                                             real_price=record.goods.shop_price)
            record.goods.goods_num -= record.nums
            record.goods.save()
        shop_carts.delete()
        return order
