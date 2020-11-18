from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals