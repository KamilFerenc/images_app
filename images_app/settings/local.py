import sys

from .base import *

print('>>>>>>>>>> local <<<<<<<<<<')


if 'test' in sys.argv:

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
