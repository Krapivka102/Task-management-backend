from django.contrib.auth import get_user_model, authenticate
from apps.core.custom_exceptions import AuthorizeError, UserDeletedError
from rest_framework.authtoken.models import Token


User = get_user_model()


class UserService:
    @staticmethod
    def authenticate(username: str, password: str) -> User:
        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthorizeError()

        if not user.is_active:
            raise UserDeletedError()

        _, _ = Token.objects.get_or_create(user=user)
        return user
