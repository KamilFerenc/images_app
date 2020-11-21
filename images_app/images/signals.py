import os

from PIL import Image
from django.conf import settings

from images_app.images.models import UserImage

from django.db.models.signals import post_save


def generate_thumbnails(sender, instance, **kwargs):
    user = instance.user
    original_image = instance.image
    dir_name = os.path.dirname(original_image.path)
    file_name = os.path.basename(original_image.name)
    for thumbnail in user.account_tier.thumbnails.all():
        outfile = os.path.join(dir_name, thumbnail.thumbnail_prefix + file_name)
        img = Image.open(original_image)
        # it is required to keep ratio - width doesn't have matter
        img.thumbnail(size=(10000, thumbnail.thumbnail_height))
        img.save(outfile)


post_save.connect(generate_thumbnails, sender=UserImage)
