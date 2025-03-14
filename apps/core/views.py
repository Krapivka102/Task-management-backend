from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from apps.core import serializers
from apps.core.services import UserService


class Auth(APIView):
    """Аутентификация пользователя."""

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        request=serializers.AuthorizeRequest, responses=serializers.AuthorizeResponse
    )
    def post(self, request):
        serializer = serializers.AuthorizeRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user, token = UserService.authenticate(username, password)

        user_data = serializers.UserSerializer(instance=user).data
        response_data = {"token": token.key, "user": user_data}

        return Response(response_data)


class Logout(APIView):
    """Выход пользователя из системы."""

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass

        return Response()
