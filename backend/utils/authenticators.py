from rest_framework.authentication import SessionAuthentication

from utils.exceptions import LoginRequired


class SessionAuthenticate(SessionAuthentication):
    def authenticate(self, request):
        # 获取 request 用户
        user = getattr(request._request, "user", None)
        if not user or not user.is_authenticated:
            raise LoginRequired()
        return user, None
