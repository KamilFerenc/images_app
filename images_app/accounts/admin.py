from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from images_app.accounts.models import CustomUser, AccountTier


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'account_tier',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'account_tier')}),
        (_('Personal info'), {'classes': ('collapse',), 'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'classes': ('collapse',),
                            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'classes': ('collapse',), 'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class AccountTierAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_image', 'generate_temp_link',)


admin.site.register(AccountTier, AccountTierAdmin)
