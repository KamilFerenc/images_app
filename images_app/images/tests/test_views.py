import datetime
from unittest import mock
from urllib.parse import urljoin

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from images_app.accounts.factories import CustomUserFactory
from images_app.images.factories import UserImageFactory, TemporaryImageLinkFactory
from images_app.images.models import TemporaryImageLink
from images_app.images.views import TemporaryImageApiView
from images_app.utils.mixins import ViewTestMixin, PrepareAccountTierMixin


class AddImageApiViewTest(ViewTestMixin, PrepareAccountTierMixin, TestCase):
    def setUp(self) -> None:
        self.premium_tier = self.create_premium_tier()
        self.user = CustomUserFactory(account_tier=self.premium_tier)
        self.image = self.create_image()
        self.url = reverse('add_image')

    def test_create_user_image(self):
        self.login(self.user)
        resp = self.client.post(self.url, data={'image': self.image})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['id'], self.user.images.first().pk)
        self.assertEqual(len(data['images']), 3)

    def test_invalid_image_extension(self):
        image_invalid_extension = self.create_image('.rgb')
        self.login(self.user)
        resp = self.client.post(self.url, data={'image': image_invalid_extension})
        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertIsNotNone(data['image'])


class GenerateTemporaryLinkApiViewTest(ViewTestMixin, PrepareAccountTierMixin, TestCase):
    def setUp(self) -> None:
        self.enterprise_tier = self.create_enterprise_tier()
        self.user = CustomUserFactory(account_tier=self.enterprise_tier)
        self.user_image = UserImageFactory(user=self.user)
        self.url = reverse('generate_link')
        self.data = {
            'user_image': self.user_image.pk,
            'time_expiration': 300
        }

    def test_user_can_generate_temp_link(self):
        self.assertTrue(self.user.account_tier.generate_temp_link)
        self.assertFalse(TemporaryImageLink.objects.filter(user_image=self.user_image).exists())
        self.login(self.user)
        resp = self.client.post(self.url, data=self.data)
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['user_image'], self.user_image.pk)
        self.assertIsNotNone(data['link'])
        self.assertTrue(TemporaryImageLink.objects.filter(user_image=self.user_image).exists())

    def test_user_can_not_generate_temp_link(self):
        self.user.account_tier = self.create_basic_tier()
        self.user.save()
        self.assertFalse(self.user.account_tier.generate_temp_link)
        self.login(self.user)
        resp = self.client.post(self.url, data=self.data)
        self.assertEqual(resp.status_code, 403)


class TemporaryImageApiViewTest(ViewTestMixin, PrepareAccountTierMixin, TestCase):
    def setUp(self) -> None:
        self.user_image = UserImageFactory()
        self.temp_link = TemporaryImageLinkFactory(user_image=self.user_image, time_expiration=300)
        self.url = reverse('temporary_image', args=(self.temp_link.link_suffix,))

    def test_valid_link(self):
        resp = self.client.get(self.url)
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['image'], urljoin(settings.BASE_URL, self.user_image.image.url))

    @mock.patch('images_app.images.views.timezone')
    def test_link_expired(self, mock_timezone_now):
        mock_timezone_now.now.return_value = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=302)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 404)

    def test_get_queryset(self):
        TemporaryImageLink.objects.all().delete()
        expired_link = TemporaryImageLinkFactory(time_expiration=0)
        valid_link = TemporaryImageLinkFactory()
        result = TemporaryImageApiView().get_queryset()
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), valid_link)
