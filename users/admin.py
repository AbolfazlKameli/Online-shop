from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('full_name', 'phone_number', 'email', 'is_admin', 'is_superuser', 'is_seller', 'id')
    list_filter = ('is_admin', 'is_superuser', 'is_seller')
    readonly_fields = ('last_login',)

    fieldsets = (
        ('Main', {'fields': ('email', 'phone_number', 'full_name', 'password', 'last_login')}),
        ('Permissions',
         {'fields': ('is_active', 'is_admin', 'is_superuser', 'is_seller', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('full_name', 'email', 'phone_number', 'password1', 'password2')}),
    )

    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


admin.site.register(User, UserAdmin)
