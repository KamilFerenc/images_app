import uuid

import factory
from factory import fuzzy

from images_app.accounts.factories import CustomUserFactory
from images_app.images.models import UserImage, TemporaryImageLink


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
