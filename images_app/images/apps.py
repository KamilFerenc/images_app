from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images_app.images'

    def ready(self):
        from images_app.images import signals
