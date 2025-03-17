from django_filters import rest_framework

from apps.core.models import Project


class ProjectFilter(rest_framework.FilterSet):
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'is_active',
            'is_private',
        )
        ordering = (
            'created_at',
            'name',
        )
