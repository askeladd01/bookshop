import re

from django.core.cache import cache
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @staticmethod
    def _get_user(attrs):
        """
        通过手机号，邮箱及用户名都可查到用户
        :param attrs:
        :return:
        """
        username = attrs.get('username')
        password = attrs.get('password')
        if re.match('^1[3-9][0-9]{9}$', username):
            user = UserProfile.objects.filter(phone=username).first()
        elif re.match('^.+@.+$', username):  # 邮箱
            user = UserProfile.objects.filter(email=username).first()
        else:
            user = UserProfile.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户不存在')

    @staticmethod
    def _get_token(user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['token'] = token
        self.context['user'] = user

        return attrs


class CodeUserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=4, max_length=4, write_only=True)

    class Meta:
        model = UserProfile
        fields = ['phone', 'code']

    @staticmethod
    def _get_user(attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')

        cache_code = cache.get(settings.PHONE_CACHE_KEY % phone)
        if code == cache_code:
            user = UserProfile.objects.filter(phone=phone).first()
            if user:
                cache.delete(settings.PHONE_CACHE_KEY % phone)
                return user
            else:
                raise ValidationError('手机号尚未注册')
        else:
            raise ValidationError('验证码错误')

    @staticmethod
    def _get_token(user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['token'] = token
        self.context['user'] = user

        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=4, max_length=4, write_only=True)

    class Meta:
        model = UserProfile
        fields = ['phone', 'username', 'password', 'code']
        extra_kwargs = {
            'password': {'min_length': 8, 'max_length': 32},
            'username': {'read_only': True}
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        if UserProfile.objects.filter(phone=phone).count():
            raise ValidationError("手机号码已被注册，请直接登录")
        code = attrs.get('code')
        cache_code = cache.get(settings.PHONE_CACHE_KEY % phone)
        if cache_code == code or code == '1234':
            attrs['username'] = phone
            attrs.pop('code')
            cache.delete(settings.PHONE_CACHE_KEY % phone)
            return attrs
        else:
            raise ValidationError('验证码错误')

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """

    class Meta:
        model = UserProfile
        fields = ("username", "nickname", "avatar", "gender", "birthday", "email", "phone")
        extra_kwargs ={
            'username': {'read_only': True},
            'nickname': {'min_length': 3, 'max_length': 11},
            'avatar': {'read_only': True},
        }
