import os

from django.test import TestCase
from django.utils import timezone

from images_app.images.factories import UserImageFactory
from images_app.images.models import image_upload_to


class ImageUploadToTest(TestCase):
    def test_image_upload_to(self):
        filename = 'test_name.jpg'
        today = timezone.now()
        user_image = UserImageFactory()
        result = image_upload_to(user_image, filename)
        expected_result = os.path.join('userdata', 'images', 'user', str(user_image.user.pk), f'{today.strftime("%Y")}',
                                       f'{today.strftime("%m")}', f'{today.strftime("%d")}', filename)
        self.assertEqual(expected_result, result)
