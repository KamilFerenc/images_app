from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

BASIC = 'basic'
PREMIUM = 'premium'
ENTERPRISE = 'enterprise'

ACCOUNT_TIERS = (
    (BASIC,  'Basic'),
    (PREMIUM,  'Premium'),
    (ENTERPRISE,  'Enterprise'),
)

ACCOUNT_TIER_RETURNED_IMAGES = {
    BASIC: [settings.PREFIX_200_PX, ],
    PREMIUM: [settings.PREFIX_200_PX, settings.PREFIX_400_PX, settings.ORIGINAL],
    ENTERPRISE: [settings.PREFIX_200_PX, settings.PREFIX_400_PX, settings.ORIGINAL]
}


class CustomUser(AbstractUser):
    account_tier = models.CharField(verbose_name=_('Account tier'), max_length=20, choices=ACCOUNT_TIERS, default=BASIC)
