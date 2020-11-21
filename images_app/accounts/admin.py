from django.contrib import admin

from images_app.accounts.models import CustomUser, AccountTier


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'account_tier', 'first_name', 'last_name', 'email')
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(CustomUser, UserAdmin)


class AccountTierAdmin(admin.ModelAdmin):
    pass


admin.site.register(AccountTier, AccountTierAdmin)
