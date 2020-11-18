import factory

from images_app.accounts.factories import CustomUserFactory
from images_app.images.models import UserImage


class UserImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserImage

    user = factory.SubFactory(CustomUserFactory)
    image = factory.django.ImageField(file_name='test_image.jpg')
