from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.core import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        'id', 'username', 'email', 'fullname', 'phone_number',
        'company_name', 'department', 'position', 'is_active', 'is_system',
    )
    search_fields = (
        'username', 'email', 'fullname', 'phone_number',
        'company_name', 'department', 'position',
    )
    list_filter = (
        'is_active', 'is_system', 'department', 'position', 'company_name',
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'patronymic', 'fullname', 'email', 'avatar', 'phone_number', 'birth_date')
        }),
        ('Организация', {
            'fields': ('company_name', 'department', 'position')
        }),
        ('Права доступа', {'fields': ('is_active', 'is_system', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('fullname',)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'is_active')
    search_fields = ('name',)
    list_filter = ('name', 'is_active')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', 'created_by', 'assigned_to', 'status')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'role')
    search_fields = ('id',)
