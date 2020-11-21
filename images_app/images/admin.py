from django.contrib import admin

from images_app.images.models import UserImage, TemporaryImageLink, ThumbnailSettings


class UserImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserImage, UserImageAdmin)


class TemporaryImageLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'expire_at', 'user_image', 'time_expiration')
    readonly_fields = ('link_suffix', 'expire_at', 'created', 'user_image', 'time_expiration')


admin.site.register(TemporaryImageLink, TemporaryImageLinkAdmin)


class ThumbnailSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail_height', 'thumbnail_prefix', 'display_name')


admin.site.register(ThumbnailSettings, ThumbnailSettingsAdmin)
