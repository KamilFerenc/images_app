from django.test import TestCase
from django.urls import reverse

from images_app.accounts.factories import CustomUserFactory
from images_app.images.factories import UserImageFactory
from images_app.utils.mixins import PrepareAccountTierMixin, ViewTestMixin


class UserDetailApiViewTest(PrepareAccountTierMixin, ViewTestMixin, TestCase):
    def setUp(self) -> None:
        self.basic_tier = self.create_basic_tier()
        self.user = CustomUserFactory(account_tier=self.basic_tier)
        self.url = reverse('detail', args=(self.user.pk,))
        self.user_image_1 = UserImageFactory(user=self.user, image__filename='test_1.jpg')
        self.user_image_2 = UserImageFactory(user=self.user, image__filename='test_2.jpg')

    def test_user_not_owner(self):
        user = CustomUserFactory()
        self.login(user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_valid_user(self):
        self.login(self.user)
        resp = self.client.get(self.url)
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data['images']), self.user.images.count())
        self.assertEqual(data['images'][0]['id'], self.user_image_1.pk)
        self.assertEqual(data['images'][1]['id'], self.user_image_2.pk)
