import os
import uuid
from urllib.parse import urljoin

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from images_app.accounts.models import ACCOUNT_TIER_RETURNED_IMAGES
from images_app.images.models import UserImage, TemporaryImageLink


class UserImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ('id', 'image', 'images',)

    def get_images(self, obj):
        request = self.context.get('request')
        image_links = []
        dir_name = os.path.dirname(obj.image.name)
        file_name = os.path.basename(obj.image.name)
        for image_prefix in ACCOUNT_TIER_RETURNED_IMAGES[request.user.account_tier]:
            thumb_file_name = os.path.join(dir_name, image_prefix + file_name)
            image_url = request.build_absolute_uri(urljoin(settings.MEDIA_URL, thumb_file_name))
            image_links.append({image_prefix: image_url})
        return image_links


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request')
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)


class TemporaryImageLinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    user_image = UserFilteredPrimaryKeyRelatedField(queryset=UserImage.objects.all())
    time_expiration = serializers.IntegerField(write_only=True, min_value=1, max_value=30000)

    class Meta:
        model = TemporaryImageLink
        fields = ('user_image', 'time_expiration', 'expire_at', 'link')
        read_only_fields = ('expire_at', 'link')

    def get_link(self, obj):
        request = self.context.get('request')
        link_images_app = request.build_absolute_uri().rsplit('/', 2)[0]
        return urljoin(f'{link_images_app}/', obj.link_suffix)

    def create(self, validated_data):
        link_suffix = str(uuid.uuid4())
        expire_at = timezone.now() + timezone.timedelta(seconds=self.validated_data['time_expiration'])
        return TemporaryImageLink.objects.create(link_suffix=link_suffix,
                                                 expire_at=expire_at,
                                                 **self.validated_data)


class TemporaryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = TemporaryImageLink
        fields = ('image',)
        lookup_field = 'link_suffix'

    def get_image(self, obj):
        return urljoin(settings.BASE_URL, obj.user_image.image.url)
