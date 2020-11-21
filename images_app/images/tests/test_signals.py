import os

from django.test import TestCase

from images_app.accounts.factories import CustomUserFactory
from images_app.images.factories import UserImageFactory
from images_app.utils.mixins import PrepareAccountTierMixin


class GenerateThumbnailsTest(TestCase, PrepareAccountTierMixin):
    def test_generate_thumbnails(self):
        file_name = 'test_img.jpg'
        # instance is created signal is executed
        user = CustomUserFactory(account_tier=self.create_premium_tier())
        user_image = UserImageFactory(image__witdh=1600, image__height=800, image__filename=file_name, user=user)
        base_dir = os.path.dirname(user_image.image.path)
        for thumbnail in user.account_tier.thumbnails.all():
            file_path = os.path.join(base_dir, thumbnail.thumbnail_prefix + file_name)
            self.assertTrue(os.path.exists(file_path))
