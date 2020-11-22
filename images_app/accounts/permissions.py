from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.request import Request

from images_app.accounts.models import CustomUser


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: CustomUser) -> bool:
        # only owner can get details view data
        return obj == request.user


class HasGenerateLinkPermission(permissions.IsAuthenticated):
    message = _('You don not have permission to generate temporary link')

    def has_permission(self, request: Request, view) -> bool:
        # only user with AccountTier: generate_temp_link=True can generate temporary link
        return getattr(request.user.account_tier, 'generate_temp_link', False)
