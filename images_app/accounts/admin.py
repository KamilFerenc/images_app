from django.contrib import admin

from images_app.accounts.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, UserAdmin)
