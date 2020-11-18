import os

from django.conf import settings
from django.test import TestCase

from images_app.images.factories import UserImageFactory
from images_app.images.signals import generate_thumbnails  # it is required to initialize signals


class GenerateThumbnailsTest(TestCase):
    def test_generate_thumbnails(self):
        file_name = 'test_img.jpg'
        # instance is created signal is executed
        user_image = UserImageFactory(image__witdh=1600, image__height=800, image__filename=file_name)
        base_dir = os.path.dirname(user_image.image.path)
        for thumbnail_setting in settings.DEFAULT_THUMBNAILS_SETTINGS:
            file_path = os.path.join(base_dir, thumbnail_setting['prefix'] + file_name)
            self.assertTrue(os.path.exists(file_path))
