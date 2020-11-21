from django.test import TestCase
from django.urls import reverse

from images_app.accounts.factories import CustomUserFactory
from images_app.accounts.models import PREMIUM
from images_app.utils.mixins import ViewTestMixin


class AddImageApiViewTest(ViewTestMixin, TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory(account_tier=PREMIUM)
        self.image = self.crete_image()
        self.url = reverse('add_image')

    def test_create_user_image(self):
        self.login(self.user)
        resp = self.client.post(self.url, data={'image': self.image})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['id'], self.user.images.first().pk)
        self.assertEqual(len(data['images']), 3)
