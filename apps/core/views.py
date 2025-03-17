from contextlib import suppress
from urllib.request import Request

from django.db import transaction
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.core import consts, filters, models, serializers
from apps.core.permissions import IsMaintainer, IsProjectMember
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
    filterset_class = filters.ProjectFilter

    def get_permissions(self) -> list:
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsMaintainer()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsProjectMember()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer: serializers.ProjectSerializer) -> None:
        with transaction.atomic():
            project = serializer.save(created_by=self.request.user)
            models.Membership.objects.get_or_create(
                user=self.request.user,
                project=project,
                role=consts.MembershipRole.MAINTAINER,
            )

    def get_queryset(self) -> QuerySet:
        return (
            models.Project.objects.filter(memberships__user=self.request.user)
            .select_related('created_by')
            .prefetch_related('members')
        )
