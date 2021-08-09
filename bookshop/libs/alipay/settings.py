import os

APPID = '2021000117696547'
APP_PRIVATE_KEY_STRING = open(os.path.join(os.path.dirname(__file__), 'pem', 'app_private_key')).read()
ALIPAY_PUBLIC_KEY_STRING = open(os.path.join(os.path.dirname(__file__), 'pem', 'alipay_public_key')).read()

SIGN_TYPE = 'RSA2'
DEBUG = True

GATEWAY = 'https://openapi.alipaydev.com/gateway.do?' if DEBUG else 'https://openapi.alipay.com/gateway.do?'
