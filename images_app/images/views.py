from django.core.cache import cache
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from images_app.accounts.permissions import HasGenerateLinkPermission
from images_app.images.models import TemporaryImageLink
from images_app.images.serializers import UserImageSerializer, TemporaryImageLinkSerializer, TemporaryImageSerializer


class AddImageApiView(CreateAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        It is require invalidate cache user detail view after adding new image.
        """
        cache.delete(request.user.username)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: UserImageSerializer) -> None:
        serializer.save(user=self.request.user)


add_image_api_view = AddImageApiView.as_view()


class GenerateTemporaryLinkApiView(CreateAPIView):
    serializer_class = TemporaryImageLinkSerializer
    permission_classes = [HasGenerateLinkPermission]


generate_temporary_link = GenerateTemporaryLinkApiView.as_view()


class TemporaryImageApiView(RetrieveAPIView):
    serializer_class = TemporaryImageSerializer
    permission_classes = [AllowAny]
    lookup_field = 'link_suffix'

    def get_queryset(self) -> QuerySet:
        return TemporaryImageLink.objects.filter(expire_at__gte=timezone.now())


temporary_image_view = TemporaryImageApiView.as_view()
