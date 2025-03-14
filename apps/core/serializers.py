from rest_framework import serializers

from apps.core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "fullname",
            "email",
        )


class AuthorizeRequest(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()


class AuthorizeResponse(serializers.Serializer):
    user = UserSerializer()
    token = serializers.CharField()
