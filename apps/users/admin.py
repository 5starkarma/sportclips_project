from django.contrib import admin

from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'password',
        'first_name',
        'last_name',
        'email',
        'phone',
        'groups',
        'tenant',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined'
    )
    filter_horizontal = (
        'groups',
    )


admin.site.register(User, UserAdmin)

