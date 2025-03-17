from rest_framework import status
from rest_framework.exceptions import APIException


class AuthorizeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'custom'
    default_detail = 'Неверные логин или пароль'


class UserDeletedError(APIException):
    status_code = status.HTTP_410_GONE
    default_code = 'custom'
    default_detail = 'Ваш аккаунт был удалён'
