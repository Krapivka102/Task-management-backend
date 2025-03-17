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


# class TaskService:
#     @staticmethod
#     def create_task(serializer: serializers, user: User) -> None:
#         project_id = serializer.validated_data.get('project_id')
#         assigned_to_id = serializer.validated_data.get('assigned_to_id')
#
#         project = models.Project.objects.filter(id=project_id).first()
#
#         if not project:
#             raise NotFound('Такого проекта не существует')
#
#         membership = models.Membership.objects.filter(
#             user=user,
#             project=project,
#         ).first()
#
#         if not membership:
#             raise PermissionDenied('Вы не являетесь участником данного проекта')
#
#         if membership.role == consts.MembershipRole.VIEWER:
#             raise PermissionDenied('Вы не можете создавать задачи в этом проекте.')
#         elif membership.role == consts.MembershipRole.DEVELOPER:
#             if assigned_to_id != user.id:
#                 raise PermissionDenied('Вы можете назначать задачу только на себя так как не имеете достаточно прав.')
#         else:
