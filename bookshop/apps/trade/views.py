from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import serializer, models


# Create your views here.


class ShoppingCartViewSet(ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        移出购物车
    put:
        修改商品数量
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == 'list':
            return serializer.ShopCartDetailSerializer
        else:
            return serializer.ShopCartSerializer

    def get_queryset(self):
        return models.ShoppingCart.objects.filter(user=self.request.user)


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_queryset(self):
        return models.OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializer.OrderDetailSerializer
        return serializer.OrderSerializer


class SuccessPayView(APIView):
    def get(self, request, *args, **kwargs):
        out_trade_no = request.query_params.get('out_trade_no')
        order = models.OrderInfo.objects.filter(order_sn=out_trade_no).first()
        if order.pay_status == 1:
            return Response(True)
        else:
            return Response(False)

    def post(self, request, *args, **kwargs):
        print(request.data)
        from bookshop.libs.alipay import alipay
        from bookshop.utils.logger import log
        data = {}
        for key, value in request.data.items():
            data[key] = value
        print(data)
        order_sn = data.get('out_trade_no', None)
        sign = data.pop('sign', None)
        success = alipay.verify(data, sign)

        print(data)

        if success:
            print(1)
            trade_no = data.get('trade_no', None)
            gmt_payment = data.get('timestamp', None)
            orders = models.OrderInfo.objects.filter(order_sn=order_sn)
            for order in orders:
                order_goods = order.goods.all()
                for good in order_goods:
                    goods = good.goods
                    goods.sold_num += good.goods_num
                    goods.save()
                order.pay_status = 1
                order.trade_no = trade_no
                order.pay_time = gmt_payment
                order.save()
                log.info(f'{order_sn}订单支付成功')
            return Response('success')
        else:
            print(111)
            log.info(f'{order_sn}订单支付异常')
            return Response('error')
