from django.db import models

from users.models import UserProfile
from goods.models import Goods


# Create your models here.
class UserFav(models.Model):
    """
    用户收藏操作
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

        # 多个字段作为一个联合唯一索引
        unique_together = ("user", "goods")

    def __str__(self):
        return self.user.username


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    province = models.CharField(max_length=100, verbose_name="省份")
    city = models.CharField(max_length=100, verbose_name="城市")
    district = models.CharField(max_length=100, verbose_name="区域")
    address = models.CharField(max_length=100, verbose_name="详细地址")
    signer_name = models.CharField(max_length=100, verbose_name="收件人")
    signer_mobile = models.CharField(max_length=11, verbose_name="手机号码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
                                       help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(max_length=100, verbose_name="主题")
    message = models.CharField("留言内容", max_length=800, help_text="留言内容")
    image = models.ImageField(upload_to="message/images/", verbose_name="上传的图片", help_text="上传图片", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject
