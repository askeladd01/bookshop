from qcloudsms_py import SmsSingleSender

from bookshop.utils.logger import log
from . import settings


def get_code():
    import random
    import string
    sms_code = ''.join(random.sample(string.digits, 4))
    return sms_code


def send_msg(phone, code):
    sender = SmsSingleSender(settings.appid, settings.appkey)
    params = [code, '5']
    try:
        result = sender.send_with_param(86, phone, settings.template_id, params, settings.sms_sign, extend="", ext="")
        if result.get('result') == 0:
            return True
        else:
            return False
    except Exception as e:
        log.error(f'【短信发送失败】--手机号 {phone}, 错误原因{str(e)}')

