from typing import Type

from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.core import consts, models


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


class IsProjectMaintainerOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Type[Model]) -> bool:
        if request.user == obj.created_by:
            return True
        membership = obj.memberships.filter(user=request.user, role=consts.MembershipRole.MAINTAINER).exists()
        return membership


class IsTaskMaintainerOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.created_by:
            return True
        membership = models.Membership.objects.filter(
            user=request.user, project=obj.project, role=consts.MembershipRole.MAINTAINER
        ).exists()
        return membership


class IsTaskAssignee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        membership = models.Membership.objects.filter(user=request.user, project=project).first()

        if not membership:
            return False

        if membership.role == consts.MembershipRole.VIEWER:
            return False

        if membership.role == consts.MembershipRole.DEVELOPER and obj.assigned_to and obj.assigned_to != request.user:
            return False

        return True
