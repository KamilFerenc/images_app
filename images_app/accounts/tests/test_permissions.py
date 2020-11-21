from django.test import TestCase
from django.urls import reverse

from images_app.accounts.factories import CustomUserFactory
from images_app.utils.mixins import ViewTestMixin


class IsOwnerTest(ViewTestMixin, TestCase):
    def setUp(self) -> None:
        self.user_1 = CustomUserFactory()
        self.user_2 = CustomUserFactory()

    def test_has_permission_false(self):
        self.login(self.user_1)
        resp = self.client.get(reverse('detail', args=(self.user_2.pk,)))
        self.assertEqual(resp.status_code, 403)

    def test_has_permission_true(self):
        self.login(self.user_1)
        resp = self.client.get(reverse('detail', args=(self.user_1.pk,)))
        self.assertEqual(resp.status_code, 200)
