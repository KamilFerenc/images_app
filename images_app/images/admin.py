from django.contrib import admin

from images_app.images.models import UserImage, TemporaryImageLink


class UserImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserImage, UserImageAdmin)


class TemporaryImageLinkAdmin(admin.ModelAdmin):
    readonly_fields = ('expire_at', 'created', 'user_image', 'time_expiration')


admin.site.register(TemporaryImageLink, TemporaryImageLinkAdmin)
