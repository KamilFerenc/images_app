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


class CustomUser(AbstractUser):
    account_tier = models.CharField(verbose_name=_('Account tier'), max_length=20, choices=ACCOUNT_TIERS, default=BASIC)
