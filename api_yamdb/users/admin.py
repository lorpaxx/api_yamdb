from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'email',
        'bio'
    )
    list_editable = ('email', 'bio')
    search_fields = ('username', 'role')
    list_filter = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
