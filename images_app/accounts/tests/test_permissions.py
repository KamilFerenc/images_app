from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.views import APIView

from images_app.accounts.factories import CustomUserFactory
from images_app.accounts.permissions import HasGenerateLinkPermission
from images_app.images.factories import UserImageFactory
from images_app.utils.mixins import ViewTestMixin, PrepareAccountTierMixin


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


class HasGenerateLinkPermissionTest(ViewTestMixin, PrepareAccountTierMixin, TestCase):
    def setUp(self) -> None:
        self.enterprise_tier = self.create_enterprise_tier()
        self.user = CustomUserFactory(account_tier=self.enterprise_tier)
        self.user_image = UserImageFactory(user=self.user)
        self.permission = HasGenerateLinkPermission()
        self.request = RequestFactory()
        self.request.user = self.user
        self.view = APIView.as_view()

    def test_has_permission_true(self):
        self.assertTrue(self.permission.has_permission(self.request, self.view))

    def test_has_permission_false(self):
        self.premium_tier = self.create_premium_tier()
        self.user.account_tier = self.premium_tier
        self.user.save()
        self.assertFalse(self.permission.has_permission(self.request, self.view))
