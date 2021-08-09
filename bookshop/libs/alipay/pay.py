from alipay import AliPay

from . import settings


alipay = AliPay(
    appid=settings.APPID,
    app_notify_url=None,
    app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
    # alipay public key, do not use your own public key!
    alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
    sign_type=settings.SIGN_TYPE,  # RSA or RSA2
    debug=settings.DEBUG  # False by default
)


gateway = settings.GATEWAY
