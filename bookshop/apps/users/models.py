from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField('昵称', max_length=32, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avatar', default='avatar/default.png')
    gender = models.IntegerField('性别', choices=((1, '男'), (2, '女')), default=1)
    email = models.EmailField('邮箱', null=True, blank=True)
    phone = models.CharField('手机', max_length=11)
    birthday = models.DateField('生日', null=True, blank=True)

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
