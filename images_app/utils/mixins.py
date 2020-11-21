import tempfile

from PIL import Image


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
