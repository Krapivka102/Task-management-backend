from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

from apps.core.custom_exceptions import AuthorizeError, UserDeletedError

User = get_user_model()


class UserService:
    @staticmethod
    def authenticate(username: str, password: str) -> tuple[User, Token]:
        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthorizeError()

        if not user.is_active:
            raise UserDeletedError()

        token, _ = Token.objects.get_or_create(user=user)
        return user, token
