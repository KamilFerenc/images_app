import uuid
from typing import List

import factory
from django.utils import timezone
from factory import fuzzy

from images_app.accounts.factories import CustomUserFactory
from images_app.images.models import UserImage, TemporaryImageLink, ThumbnailSettings


class UserImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserImage

    user = factory.SubFactory(CustomUserFactory)
    image = factory.django.ImageField(file_name='test_image.jpg')


class TemporaryImageLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemporaryImageLink

    link_suffix = str(uuid.uuid4())
    user_image = factory.SubFactory(UserImageFactory)
    time_expiration = fuzzy.FuzzyInteger(300, 30000)

    @factory.post_generation
    def expire_at(self, create: bool, extracted: List = None, **kwargs):
        if not create:
            return
        self.expire_at = timezone.now() + timezone.timedelta(seconds=self.time_expiration)
        self.save()


class ThumbnailSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ThumbnailSettings
    thumbnail_height = fuzzy.FuzzyInteger(200, 800)
    thumbnail_prefix = factory.Sequence(lambda n: f'{n}_px_')
    display_name = factory.Sequence(lambda n: f'{n} px')
