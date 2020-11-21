import tempfile

from PIL import Image

from images_app.accounts.factories import AccountTierFactory
from images_app.images.factories import ThumbnailSettingsFactory


class ViewTestMixin:
    def login(self, user, password='pass'):
        value = self.client.login(username=user.username, password=password)
        self.assertTrue(value)

    @staticmethod
    def crete_image():
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image = Image.new('RGB', (600, 600), )
        image.save(tmp_file.name, 'jpeg')
        return tmp_file


class PrepareAccountTierMixin:
    @staticmethod
    def prepare_thumbnails():
        th_settings_200_px = ThumbnailSettingsFactory(thumbnail_height=200,
                                                      thumbnail_prefix='200_px_',
                                                      display_name='200 px')
        th_settings_400_px = ThumbnailSettingsFactory(thumbnail_height=400,
                                                      thumbnail_prefix='400_px_',
                                                      display_name='400 px')
        return [th_settings_200_px, th_settings_400_px]

    def crate_basic_tier(self):
        return AccountTierFactory(title='Basic', thumbnails=self.prepare_thumbnails())

    def crate_premium_tier(self):
        return AccountTierFactory(title='Premium', original_image=True, thumbnails=self.prepare_thumbnails())

    def crate_enterprise_tier(self):
        return AccountTierFactory(title='Enterprise',
                                  original_image=True,
                                  generate_temp_link=True,
                                  thumbnails=self.prepare_thumbnails())
