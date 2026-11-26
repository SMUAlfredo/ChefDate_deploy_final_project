"""Persistent local SQLite settings for the ChefDate demo."""

from .settings_base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3-demo',
    },
}
