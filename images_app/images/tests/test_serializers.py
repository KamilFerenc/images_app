from urllib.parse import urljoin

from django.conf import settings
from django.test import RequestFactory
from django.test import TestCase

from images_app.accounts.factories import CustomUserFactory
from images_app.images.factories import UserImageFactory, TemporaryImageLinkFactory
from images_app.images.models import UserImage, TemporaryImageLink
from images_app.images.serializers import (
    UserImageSerializer, UserFilteredPrimaryKeyRelatedField, TemporaryImageLinkSerializer, TemporaryImageSerializer
)


class UserImageSerializerTest(TestCase):
    def setUp(self) -> None:
        self.image = UserImageFactory()
        self.serializer = UserImageSerializer

    def test_get_images(self):
        pass


class UserFilteredPrimaryKeyRelatedFieldTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory()
        self.image_1 = UserImageFactory()
        self.image_2 = UserImageFactory(user=self.user)
        self.image_3 = UserImageFactory()
        self.request = RequestFactory()
        self.request.user = self.user
        self.queryset = UserImage.objects.all()
        self.user_filtered_primary_key = UserFilteredPrimaryKeyRelatedField(queryset=self.queryset)
        self.context = {'request': self.request}
        self.temporary_image_serializer = TemporaryImageLinkSerializer

    def test_get_queryset(self):
        self.user_filtered_primary_key.parent = self.temporary_image_serializer(context=self.context)
        result = self.user_filtered_primary_key.get_queryset()
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.image_2)

    def test_get_queryset_request_none(self):
        self.user_filtered_primary_key.parent = self.temporary_image_serializer()
        self.assertIsNone(self.user_filtered_primary_key.get_queryset())


class TemporaryImageLinkSerializerTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory()
        self.user_image = UserImageFactory(user=self.user)
        self.serializer = TemporaryImageLinkSerializer
        self.data = {'user_image': self.user_image.pk,
                     'time_expiration': 1234}
        self.request = RequestFactory()
        self.request.user = self.user

    def test_create(self):
        self.assertFalse(TemporaryImageLink.objects.exists())
        serializer = self.serializer(data=self.data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        temp_link = serializer.save()
        self.assertEqual(temp_link.user_image, self.user_image)
        self.assertEqual(temp_link.time_expiration, self.data['time_expiration'])

    def test_create_image_not_belong_to_user(self):
        self.assertFalse(TemporaryImageLink.objects.exists())
        user_image = UserImageFactory()
        self.data['user_image'] = user_image.pk
        serializer = self.serializer(data=self.data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertFalse(TemporaryImageLink.objects.exists())

    def test_get_link(self):
        request = self.request.request()
        temp_link = TemporaryImageLinkFactory(user_image__user=self.user)
        result = self.serializer(context={'request': request}).get_link(temp_link)
        self.assertEqual(urljoin(f'{request.build_absolute_uri().rsplit("/", 2)[0]}/', temp_link.link_suffix), result)


class TemporaryImageSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = TemporaryImageSerializer
        self.temp_link = TemporaryImageLinkFactory()
        self.request = RequestFactory()

    def test_get_image(self):
        request = self.request.request()
        result = self.serializer(context={'request': request}).get_image(self.temp_link)
        self.assertEqual(urljoin(settings.BASE_URL, self.temp_link.user_image.image.url), result)
