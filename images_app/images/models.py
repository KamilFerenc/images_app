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
    image = models.ForeignKey('UserImage', verbose_name=_('Image'), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
