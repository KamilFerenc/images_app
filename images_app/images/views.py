from django.utils import timezone
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from images_app.accounts.permissions import IsOwner
from images_app.images.models import TemporaryImageLink
from images_app.images.serializers import UserImageSerializer, TemporaryImageLinkSerializer, TemporaryImageSerializer


class AddImageApiView(CreateAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


add_image_api_view = AddImageApiView.as_view()


class GenerateTemporaryLinkApiView(CreateAPIView):
    serializer_class = TemporaryImageLinkSerializer
    permission_classes = [IsOwner]


generate_temporary_link = GenerateTemporaryLinkApiView.as_view()


class TemporaryImageApiView(RetrieveAPIView):
    serializer_class = TemporaryImageSerializer
    permission_classes = [AllowAny]
    queryset = TemporaryImageLink.objects.filter(expire_at__gte=timezone.now())
    lookup_field = 'link_suffix'


temporary_image_view = TemporaryImageApiView.as_view()
