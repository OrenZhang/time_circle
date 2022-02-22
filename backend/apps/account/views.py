from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.account.serializers import LoginFormSerializer, UserInfoSerializer
from utils.exceptions import LoginFailed
from utils.throttlers import LoginThrottler

USER_MODEL = get_user_model()


class UserView(GenericViewSet):
    """用户信息"""

    queryset = USER_MODEL.objects.all()
    serializer_class = UserInfoSerializer

    @action(
        methods=["POST"],
        detail=False,
        authentication_classes=[],
        throttle_classes=[LoginThrottler],
    )
    def sign_in(self, request, *args, **kwargs):
        serializer = LoginFormSerializer(data=request.data)
        if not serializer.is_valid():
            raise LoginFailed("登陆表单有误")
        user = auth.authenticate(**serializer.validated_data)
        if user is None:
            raise LoginFailed("用户名或密码错误")
        auth.login(request, user)
        return Response()

    @action(methods=["GET"], detail=False)
    def user_info(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
