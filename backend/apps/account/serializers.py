from django.contrib.auth import get_user_model
from rest_framework import serializers

USER_MODEL = get_user_model()


class LoginFormSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ["id", "username", "last_login"]
