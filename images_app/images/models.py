import os
import datetime

from django.core.validators import FileExtensionValidator
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
