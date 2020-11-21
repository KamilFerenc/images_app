from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

BASIC = 'basic'
PREMIUM = 'premium'
ENTERPRISE = 'enterprise'

ACCOUNT_TIERS = (
    (BASIC, 'Basic'),
    (PREMIUM, 'Premium'),
    (ENTERPRISE, 'Enterprise'),
)

ACCOUNT_TIER_RETURNED_IMAGES = {
    BASIC: [settings.PREFIX_200_PX, ],
    PREMIUM: [settings.PREFIX_200_PX, settings.PREFIX_400_PX, settings.ORIGINAL],
    ENTERPRISE: [settings.PREFIX_200_PX, settings.PREFIX_400_PX, settings.ORIGINAL]
}

ORIGINAL_IMAGE_DISPlAY_NAME = 'Original'


class CustomUser(AbstractUser):
    account_tier = models.ForeignKey('AccountTier', verbose_name=_('Account tier'), null=True,
                                     on_delete=models.SET_NULL)


class AccountTier(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=20, unique=True)
    original_image = models.BooleanField(verbose_name=_('Original image'), default=False,
                                         help_text=_('If True, user will get link to original image in response'))
    generate_temp_link = models.BooleanField(verbose_name=_('Generate temporary link'), default=False,
                                             help_text=_('If True, user will have option to generate temporary link'))
    thumbnails = models.ManyToManyField('images.ThumbnailSettings', verbose_name=_('Thumbnails'),
                                        related_name='account_tiers')

    def __str__(self):
        return self.title
