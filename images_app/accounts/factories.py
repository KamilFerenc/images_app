import factory

from images_app.accounts.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
