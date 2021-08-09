from rest_framework.views import exception_handler
from .response import APIResponse
from .logger import log


def common_exception_handler(exc, context):
    """
    重写drf的异常处理方法，将drf无法处理的异常统一输出格式
    """
    log.error(f"view:{context.get('view').__class__.__name__},{str(exc)}")  # 记录错误日志
    ret = exception_handler(exc, context)
    if not ret:
        return APIResponse(code=0, msg='error', result=str(exc))
    else:
        return APIResponse(code=0, msg='error', result=ret.data)
