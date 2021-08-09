from rest_framework.response import Response


class APIResponse(Response):
    """
    封装响应方法，添加提示信息
    """
    def __init__(self, code=1, msg='ok', result=None, status=None, headers=None, content_type=None, **kwargs):
        dic = {
            'code': code,
            'msg': msg,
        }
        if result:
            dic['result'] = result
        dic.update(kwargs)
        super(APIResponse, self).__init__(data=dic, status=status, headers=headers, content_type=content_type)
