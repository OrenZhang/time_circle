from django.contrib.auth.models import AnonymousUser
from rest_framework.throttling import SimpleRateThrottle

from utils.tools import get_ip


class LoginThrottler(SimpleRateThrottle):
    scope = "login_scope"

    def get_cache_key(self, request, view):
        username = str(request.data.get("username", str(AnonymousUser)))
        return f"{self.__class__.__name__}:{get_ip(request)}:{username}"
