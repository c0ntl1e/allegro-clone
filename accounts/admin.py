from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Marketplace', {
            'fields': ('role', 'company'),
        }),
    )

    list_display = (
        'username',
        'email',
        'role',
        'company',
        'is_staff',
    )