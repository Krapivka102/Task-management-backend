from typing import Type

from django.db.models import Model
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.core import consts, models


class IsMaintainer(BasePermission):
    """
    Проверяет, является ли пользователь Maintainer.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Type[Model]) -> bool:
        if not request.user.is_authenticated:
            return False

        project = getattr(obj, 'project', obj)
        return models.Membership.objects.filter(
            user=request.user,
            project=project,
            role=consts.MembershipRole.MAINTAINER,
        ).exists()


class IsProjectMember(BasePermission):
    """
    Проверяет, является ли пользователь участником проекта.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Type[Model]) -> bool:
        if not request.user.is_authenticated:
            return False

        project = getattr(obj, 'project', obj)
        return models.Membership.objects.filter(
            user=request.user,
            project=project,
        ).exists()
