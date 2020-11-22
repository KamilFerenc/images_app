from django.test import TestCase

from images_app.accounts.factories import CustomUserFactory
from images_app.utils.mixins import ViewTestMixin


class ViewTestMixinTest(TestCase):
    def test_login_true(self):
        user = CustomUserFactory()
        view_test_mixin = ViewTestMixin()
        view_test_mixin.client = self.client
        view_test_mixin.assertTrue = self.assertTrue
        self.assertIsNone(view_test_mixin.login(user))

    def test_create_image(self):
        result = ViewTestMixin().create_image()
        self.assertIsNotNone(result)
        self.assertTrue(result.name.endswith('.jpg'))
