from django.contrib import admin
from core import models
from django.contrib.auth.admin import UserAdmin

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('username',)
    list_filter = ('username',)
