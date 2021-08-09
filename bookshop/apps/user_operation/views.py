from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models, serializer


class UserFavViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return models.UserFav.objects.filter(user=self.request.user)

    # 设置动态的Serializer
    def get_serializer_class(self):
        if self.action == "list":
            return serializer.UserFavDetailSerializer
        elif self.action == "create":
            return serializer.UserFavSerializer

        return serializer.UserFavSerializer


class LeavingMessageViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言功能
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = serializer.LeavingMessageSerializer

    # 只能看到自己的留言
    def get_queryset(self):
        return models.UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = serializer.AddressSerializer

    def get_queryset(self):
        return models.UserAddress.objects.filter(user=self.request.user)
