from django.contrib import admin

from users.models import User, Role, API


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'avatar']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(API)
class APIAdmin(admin.ModelAdmin):
    list_display = ['name', 'api']
