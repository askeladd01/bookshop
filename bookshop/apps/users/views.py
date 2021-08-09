import re

from django.core.cache import cache
from django.conf import settings
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from bookshop.utils.response import APIResponse
from .throttlings import SmsThrottling
from .models import UserProfile
from .serializer import UserRegisterSerializer, UserSerializer, CodeUserSerializer, UserDetailSerializer


# Create your views here.


class SendSmsView(APIView):
    throttle_classes = [SmsThrottling]

    def post(self, request, *args, **kwargs):
        from bookshop.libs.tx_sms.send import get_code, send_msg
        phone = request.data.get('phone')

        if not re.match('^1[3-9][0-9]{9}', phone):
            return APIResponse(code=0, msg='手机号码格式不正确')
        code = get_code()
        result = send_msg(phone, code)
        # 保存验证码
        cache.set(settings.PHONE_CACHE_KEY % phone, code, 300)

        if result:
            return APIResponse(code=1, msg='验证码发送成功')
        else:
            return APIResponse(code=0, msg='验证码发送失败')


class RegisterView(CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super(RegisterView, self).create(request, *args, **kwargs)
        username = response.data.get('username')
        return APIResponse(code=1, msg='注册成功', username=username)


class LoginView(ViewSet):
    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username
            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)

    @action(detail=False)
    def check_phone(self, request, *args, **kwargs):
        import re
        phone = request.query_params.get('phone')
        if not re.match('^1[3-9][0-9]{9}', phone):
            return APIResponse(code=0, msg='手机号不合法')
        try:
            UserProfile.objects.get(phone=phone)
            return APIResponse(code=1)
        except:
            return APIResponse(code=0, msg='手机号不存在')

    @action(methods=['POST'], detail=False)
    def code_login(self, request, *args, **kwargs):

        ser = CodeUserSerializer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username
            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)


class UserView(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user.username)

    serializer_class = UserDetailSerializer

    # 重写该方法，不管传什么id，都只返回当前用户
    def get_object(self):
        return self.request.user


