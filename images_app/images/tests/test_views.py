from django.test import TestCase
from django.urls import reverse

from images_app.accounts.factories import CustomUserFactory
from images_app.utils.mixins import ViewTestMixin, PrepareAccountTierMixin


class AddImageApiViewTest(ViewTestMixin, PrepareAccountTierMixin, TestCase):
    def setUp(self) -> None:
        self.premium_tier = self.crate_premium_tier()
        self.user = CustomUserFactory(account_tier=self.premium_tier)
        self.image = self.crete_image()
        self.url = reverse('add_image')

    def test_create_user_image(self):
        self.login(self.user)
        resp = self.client.post(self.url, data={'image': self.image})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['id'], self.user.images.first().pk)
        self.assertEqual(len(data['images']), 3)
