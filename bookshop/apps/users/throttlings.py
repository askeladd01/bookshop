from rest_framework.throttling import SimpleRateThrottle


class SmsThrottling(SimpleRateThrottle):
    scope = 'sms'

    def get_cache_key(self, request, view):
        phone = request.query_params.get('phone')
        return self.cache_format%{'scope': self.scope, 'ident': phone}
