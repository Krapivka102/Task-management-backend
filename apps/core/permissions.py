from rest_framework.permissions import BasePermission
from apps.core import models, consts


class IsMaintainer(BasePermission):
    """
    Проверяет, является ли пользователь Maintainer.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        project_pk = view.kwargs.get("pk")
        return models.Membership.objects.filter(
            user=request.user,
            project_id=project_pk,
            role=consts.MembershipRole.MAINTAINER,
        ).exists()
