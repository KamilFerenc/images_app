from django.test import TestCase

from images_app.accounts.factories import AccountTierFactory


class AccountTierTest(TestCase):
    def test__str__(self):
        account_tier = AccountTierFactory()
        self.assertEqual(account_tier.title, str(account_tier))
