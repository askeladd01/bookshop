from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x(ot=^93$etn15ks5$ryww670&3w61xpu*)i!ei0$i*7dr!u=='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bookshop',
        'USER': 'root',
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# 支付宝沙箱环境
# 后台基URL
BASE_URL = 'http://127.0.0.1:8000'
# 前台基URL
SHOP_URL = 'http://127.0.0.1:8080'
# 支付宝同步异步回调接口配置
# 后台异步回调接口
NOTIFY_URL = BASE_URL + "/trade/success/"
# 前台同步回调接口，没有 / 结尾
RETURN_URL = SHOP_URL + "/pay/success"
