import os
import uuid
from typing import List, Union, Dict
from urllib.parse import urljoin

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import serializers

from images_app.accounts.models import ORIGINAL_IMAGE_DISPlAY_NAME
from images_app.images.models import UserImage, TemporaryImageLink, IMAGE_ALLOWED_EXTENSION


class UserImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True,
                                   validators=[FileExtensionValidator(allowed_extensions=IMAGE_ALLOWED_EXTENSION)])
    images = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ('id', 'image', 'images',)

    def get_images(self, obj: UserImage) -> List:
        """
        Get image and generated thumbnails for user based on the AccountTier type.
        """
        request = self.context.get('request')
        image_links = []
        dir_name = os.path.dirname(obj.image.name)
        file_name = os.path.basename(obj.image.name)
        for thumbnail in request.user.account_tier.thumbnails.all():
            thumbnail_file_name = os.path.join(dir_name, thumbnail.thumbnail_prefix + file_name)
            image_url = request.build_absolute_uri(urljoin(settings.MEDIA_URL, thumbnail_file_name))
            image_links.append({thumbnail.display_name: image_url})
        if request.user.account_tier.original_image:
            image_links.append({ORIGINAL_IMAGE_DISPlAY_NAME: request.build_absolute_uri(obj.image.url)})
        return image_links


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self) -> Union[QuerySet, None]:
        request = self.context.get('request')
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)


class TemporaryImageLinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    user_image = UserFilteredPrimaryKeyRelatedField(queryset=UserImage.objects.all())
    time_expiration = serializers.IntegerField(write_only=True, min_value=300, max_value=30000)

    class Meta:
        model = TemporaryImageLink
        fields = ('user_image', 'time_expiration', 'expire_at', 'link')
        read_only_fields = ('expire_at', 'link')

    def get_link(self, obj: TemporaryImageLink) -> str:
        """
        Return link for the TemporaryImageLink object
        """
        request = self.context.get('request')
        link_images_app = request.build_absolute_uri().rstrip('/').rsplit('/', 1)[0]
        return urljoin(f'{link_images_app}/', obj.link_suffix)

    def create(self, validated_data: Dict[str, Union[int, str]]) -> TemporaryImageLink:
        """
        When object is saved generate random value (link_suffix) and set expire_at automatically.
        """
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

    def get_image(self, obj: TemporaryImageLink) -> str:
        """
        Return link to image for which TemporaryImageLink has been generated.
        """
        return urljoin(settings.BASE_URL, obj.user_image.image.url)
