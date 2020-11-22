from typing import List

import factory

from images_app.accounts.models import CustomUser, AccountTier


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
    username = factory.Sequence(lambda n: f'user_{n}')
    password = factory.PostGenerationMethodCall('set_password', 'pass')


class AccountTierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountTier
    title = factory.Sequence(lambda n: f'Title_{n}')

    @factory.post_generation
    def thumbnails(self, create: bool, extracted: List = None, **kwargs) -> None:
        if not create:
            return
        if extracted:
            for thumbnail in extracted:
                self.thumbnails.add(thumbnail)
