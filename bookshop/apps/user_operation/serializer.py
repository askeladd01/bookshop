from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from goods.serializer import GoodsSerializer
from . import models


class UserFavDetailSerializer(serializers.ModelSerializer):
    # 通过goods_id拿到商品信息。就需要嵌套的Serializer
    goods = GoodsSerializer()

    class Meta:
        model = models.UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.UserFav
        # 使用validate方式实现唯一联合
        validators = [
            UniqueTogetherValidator(
                queryset=models.UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.UserLeavingMessage
        fields = ("id", "user", "message_type", "subject", "message", "image", "create_time")
        extra_kwargs = {
            'create_time': {'read_only': True}
        }


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "signer_mobile")
