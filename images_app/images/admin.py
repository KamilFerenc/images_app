from django.contrib import admin

from images_app.images.models import UserImage


class UserImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserImage, UserImageAdmin)
