from django.utils.translation import gettext_lazy as _
from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # only owner can get details view data
        return obj == request.user


class HasGenerateLinkPermission(permissions.IsAuthenticated):
    message = _('You don not have permission to generate temporary link')

    def has_permission(self, request, view):
        # only user with AccountTier: generate_temp_link=True can generate temporary link
        return getattr(request.user.account_tier, 'generate_temp_link', False)
