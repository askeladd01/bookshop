import os
from alipay import AliPay

APPID = '2021000117696547'
APP_PRIVATE_KEY_STRING = open(r'C:\Users\guoxu\PycharmProjects\bookshop\bookshop\libs\alipay\pem\app_private_key').read()

ALIPAY_PUBLIC_KEY_STRING = open(r'C:\Users\guoxu\PycharmProjects\bookshop\bookshop\libs\alipay\pem\alipay_public_key').read()

# 后台基URL
BASE_URL = 'http://127.0.0.1:8000'
# 前台基URL
SHOP_URL = 'http://127.0.0.1:8080'
# 后台异步回调接口
NOTIFY_URL = BASE_URL + "/order/success/"
# 前台同步回调接口，没有 / 结尾
RETURN_URL = SHOP_URL + "/pay/success"


SIGN_TYPE = 'RSA2'
DEBUG = True

GATEWAY = 'https://openapi.alipaydev.com/gateway.do?' if DEBUG else 'https://openapi.alipay.com/gateway.do?'

alipay = AliPay(
    appid=APPID,
    app_notify_url=None,  # the default notify path
    app_private_key_string=APP_PRIVATE_KEY_STRING,
    # alipay public key, do not use your own public key!
    alipay_public_key_string=ALIPAY_PUBLIC_KEY_STRING,
    sign_type=SIGN_TYPE,  # RSA or RSA2
    debug=DEBUG  # False by default
)

gateway = GATEWAY

order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no=213,
    total_amount=123,
    subject="123",
    return_url=RETURN_URL,  # get回调，前台地址
    notify_url=NOTIFY_URL  # post回调，后台地址
)
u = gateway + order_string
print(u)
