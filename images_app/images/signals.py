import os

from PIL import Image
from django.conf import settings

from images_app.images.models import UserImage

from django.db.models.signals import post_save


def generate_thumbnails(sender, instance, **kwargs):
    original_image = instance.image
    dir_name = os.path.dirname(original_image.path)
    file_name = os.path.basename(original_image.name)
    for thumbnail_data in settings.DEFAULT_THUMBNAILS_SETTINGS:
        outfile = os.path.join(dir_name, thumbnail_data['prefix'] + file_name)
        img = Image.open(original_image)
        img.thumbnail(thumbnail_data['size'])
        img.save(outfile)


post_save.connect(generate_thumbnails, sender=UserImage)
