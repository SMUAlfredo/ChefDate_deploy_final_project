import os
from unittest.mock import patch

# Load shared Django settings without reading the local Neon credentials.
with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://tests.invalid/chefdate'}):
    from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
