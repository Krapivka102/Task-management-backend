from django.contrib import admin

from apps.core import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    search_fields = ("username",)
    list_filter = ("username",)


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "group", "created_by", "is_active")
    search_fields = ("name",)
    list_filter = ("name", "is_active")


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "created_by", "assigned_to", "status")
    search_fields = ("title",)
    list_filter = ("title",)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "author")
    search_fields = ("id",)


@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "comment", "uploaded_by")
    search_fields = ("id",)
