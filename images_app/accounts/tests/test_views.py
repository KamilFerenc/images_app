from django.conf import settings
from django.test import TestCase, override_settings
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

    @override_settings(CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'cache:11211',
            'TIMEOUT': 1 * settings.DAY
        }
    })
    def test_cache_activated(self):
        base_images_quantity = self.user.images.count()
        self.login(self.user)
        resp_1 = self.client.get(self.url)
        data_1 = resp_1.json()
        self.assertEqual(len(data_1['images']), base_images_quantity)
        # add UserImage - response should be get from cache
        self.user_image_3 = UserImageFactory(user=self.user, image__filename='test_3.jpg')
        resp_2 = self.client.get(self.url)
        data_2 = resp_2.json()
        self.assertEqual(data_1, data_2)

    def test_cache_not_activated(self):
        base_images_quantity = self.user.images.count()
        self.login(self.user)
        resp_1 = self.client.get(self.url)
        data_1 = resp_1.json()
        self.assertEqual(len(data_1['images']), base_images_quantity)
        # add UserImage - response should not be get from cache
        self.user_image_3 = UserImageFactory(user=self.user, image__filename='test_3.jpg')
        resp_2 = self.client.get(self.url)
        data_2 = resp_2.json()
        self.assertNotEqual(data_1, data_2)
