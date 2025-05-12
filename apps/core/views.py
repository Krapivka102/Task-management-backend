from contextlib import suppress
from urllib.request import Request

from django.db import transaction
from django.db.models import Prefetch, QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.core import consts, filters, models, serializers
from apps.core.permissions import IsProjectMaintainerOrOwner, IsProjectMember, IsTaskAssignee, IsTaskMaintainerOrOwner
from apps.core.services import UserService


class Auth(APIView):
    """Аутентификация пользователя."""

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(request=serializers.AuthorizeRequest, responses=serializers.AuthorizeResponse)
    def post(self, request: Request) -> Response:
        serializer = serializers.AuthorizeRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user, token = UserService.authenticate(username, password)

        user_data = serializers.UserSerializer(instance=user).data
        response_data = {'token': token.key, 'user': user_data}

        return Response(response_data)


class Logout(APIView):
    """Выход пользователя из системы."""

    def post(self, request: Request) -> Response:
        with suppress(Token.DoesNotExist):
            request.user.auth_token.delete()

        return Response()


class ProjectViewSet(ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = filters.ProjectFilter

    def get_queryset(self) -> QuerySet:
        return (
            models.Project.objects.filter(memberships__user=self.request.user)
            .select_related('created_by')
            .prefetch_related(
                Prefetch('memberships', queryset=models.Membership.objects.filter(user=self.request.user))
            )
        )

    def get_permissions(self) -> list:
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsProjectMaintainerOrOwner()]
        elif self.action in ['list', 'retrieve']:
            return [IsProjectMember()]
        return super().get_permissions()

    def perform_create(self, serializer: serializers.ProjectSerializer) -> None:
        with transaction.atomic():
            project = serializer.save(created_by=self.request.user)
            models.Membership.objects.get_or_create(
                user=self.request.user,
                project=project,
                role=consts.MembershipRole.MAINTAINER,
            )


class TaskViewSet(ModelViewSet):
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return (
            models.Task.objects.filter(project__memberships__user=self.request.user)
            .select_related('project', 'assigned_to')
            .prefetch_related('project__memberships')
        )

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsTaskMaintainerOrOwner()]
        elif self.action == 'create':
            return [IsTaskAssignee()]
        return super().get_permissions()

    def perform_create(self, serializer: serializers.TaskSerializer) -> None:
        project_id = self.request.data.get('project_id')
        assigned_to_id = self.request.data.get('assigned_to_id')

        project = models.Project.objects.filter(id=project_id).first()
        if not project:
            raise NotFound('Такого проекта не существует.')

        user = models.User.objects.filter(id=assigned_to_id).first()
        if not user:
            raise NotFound('Такого юзера не существует.')

        membership = models.Membership.objects.filter(user=self.request.user, project=project).first()

        if membership.role == consts.MembershipRole.DEVELOPER and self.request.user.id != assigned_to_id:
            raise PermissionDenied('Разработчик может назначать задачу только себе.')

        if not membership:
            raise PermissionDenied('Вы не являетесь участником проекта.')

        with transaction.atomic():
            serializer.save(created_by=self.request.user)
