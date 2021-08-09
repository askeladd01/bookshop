from django.db import models

from users.models import UserProfile
from goods.models import Goods


# Create your models here.
class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    nums = models.IntegerField(default=1, verbose_name="购买数量")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return f"{self.goods.name}({self.nums})"


class OrderInfo(models.Model):
    """
    订单信息
    """
    ORDER_STATUS = (
        (0, "待支付"),
        (1, "支付成功"),
        (2, "取消订单"),
        (3, "超时关闭"),
    )
    PAY_TYPE = (
        (1, "支付宝"),
        (2, "微信"),
    )

    subject = models.CharField(max_length=150, verbose_name="订单标题")
    # unique订单号唯一
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单编号")
    # 支付宝支付时的交易号与本系统进行关联
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="交易号")
    pay_status = models.SmallIntegerField(choices=ORDER_STATUS, default=0, verbose_name="订单状态")
    # 订单的支付类型
    pay_type = models.SmallIntegerField(choices=PAY_TYPE, default=1, verbose_name="支付类型")
    post_script = models.CharField(max_length=200, null=True, blank=True, verbose_name="订单留言")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 用户的基本信息
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    address = models.CharField(max_length=100,  verbose_name="收货地址")
    signer_name = models.CharField(max_length=20,  verbose_name="收件人")
    singer_mobile = models.CharField(max_length=11, verbose_name="联系电话")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单内的商品详情
    """
    # 一个订单对应多个商品，所以添加外键
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单信息", related_name="goods")
    # 两个外键形成一张关联表
    goods = models.ForeignKey(Goods, on_delete=models.SET_NULL, null=True, db_constraint=False, verbose_name="商品")
    real_price = models.FloatField("商品实价", default=0.0)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
