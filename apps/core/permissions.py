from typing import Type

from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.core import consts, models


class IsMaintainer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь Maintainer.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Type[Model]) -> bool:
        project = getattr(obj, 'project', obj)
        return models.Membership.objects.filter(
            user=request.user,
            project=project,
            role=consts.MembershipRole.MAINTAINER,
        ).exists()


class IsProjectMember(permissions.BasePermission):
    """
    Проверяет, является ли пользователь участником проекта.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Type[Model]) -> bool:
        project = getattr(obj, 'project', obj)
        return models.Membership.objects.filter(
            user=request.user,
            project=project,
        ).exists()


class IsMaintainerOrDeveloper(permissions.BasePermission):
    """Проверяет, является ли пользователь Maintainer или Developer проекта."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        project_id = request.data.get('project_id') or view.kwargs.get('pk')
        if not project_id:
            return False

        return models.Membership.objects.filter(
            user=request.user,
            project_id=project_id,
            role__in=[consts.MembershipRole.MAINTAINER, consts.MembershipRole.DEVELOPER],
        ).exists()


class TaskPermission(permissions.BasePermission):
    """
    Кастомное разрешение для управления доступом к задачам в проекте.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Type[Model]) -> bool:
        """Проверяем доступ к конкретной задаче (PUT, PATCH, DELETE)"""
        user = request.user
        role = models.Membership.get_user_role(user, obj.project)

        if request.method in permissions.SAFE_METHODS:
            return True

        if role == consts.MembershipRole.DEVELOPER:
            return obj.created_by == user

        return role == consts.MembershipRole.MAINTAINER

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Проверяем доступ на уровне списка (POST, GET, LIST)"""
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        project_id = request.data.get('project_id')

        if not project_id:
            return False

        role = models.Membership.get_user_role(user, project_id)

        if role == consts.MembershipRole.DEVELOPER:
            assigned_to_id = request.data.get('assigned_to_id')
            return assigned_to_id is None or int(assigned_to_id) == user.id

        return role == consts.MembershipRole.MAINTAINER
