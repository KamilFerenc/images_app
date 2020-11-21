import os
import datetime

from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

IMAGE_ALLOWED_EXTENSION = ['jpg', 'png']


def image_upload_to(instance, filename):
    today = datetime.datetime.today()
    return os.path.join('userdata', 'images', 'user', str(instance.user.pk),  f'{today.strftime("%Y")}',
                        f'{today.strftime("%m")}', f'{today.strftime("%d")}', filename)


class UserImage(models.Model):
    user = models.ForeignKey('accounts.CustomUser', verbose_name=_('User'),
                             related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('Image'), upload_to=image_upload_to,
                              validators=[FileExtensionValidator(allowed_extensions=IMAGE_ALLOWED_EXTENSION)])
    modified = models.DateTimeField(verbose_name=_('Modified'), auto_now=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)


class TemporaryImageLink(models.Model):
    link_suffix = models.CharField(verbose_name=_('Link suffix'), max_length=100)
    time_expiration = models.PositiveIntegerField(verbose_name=_('Time expiration'),
                                                  validators=[MinValueValidator(300), MaxValueValidator(30000)])
    expire_at = models.DateTimeField(verbose_name=_('Expire at'), blank=True, null=True)
    user_image = models.ForeignKey('UserImage', verbose_name=_('User image'), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)


class ThumbnailSettings(models.Model):
    thumbnail_height = models.PositiveIntegerField(verbose_name=_('Thumbnail height'), unique=True)
    thumbnail_prefix = models.CharField(verbose_name=_('Thumbnail prefix'), unique=True, max_length=10,
                                        help_text=_('Thumbnail file name will be start for this prefix'))
    display_name = models.CharField(
        verbose_name=_('Display name'), blank=True, max_length=20,
        help_text=_('Value used as a key value in response in order to recognize thumbnail')
    )

    def __str__(self):
        return f'Thumbnail height {self.thumbnail_height} px'
