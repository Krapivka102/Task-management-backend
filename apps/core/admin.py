from django.contrib import admin

from apps.core import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    search_fields = ("username",)
    list_filter = ("username",)
