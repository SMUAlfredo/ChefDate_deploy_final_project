"""Local development settings."""

import os

import certifi
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import dotenv_values

from .settings_base import *


def _database_config():
    database_url = os.environ.get('DATABASE_URL')
    if database_url is None:
        database_url = dotenv_values(BASE_DIR / '.env', interpolate=False).get('DATABASE_URL')

    if database_url is None:
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }

    try:
        database = dj_database_url.parse(database_url)
    except ValueError:
        raise ImproperlyConfigured('DATABASE_URL must be a valid PostgreSQL URL.') from None

    if database['ENGINE'] != 'django.db.backends.postgresql' or not database.get('HOST'):
        raise ImproperlyConfigured('DATABASE_URL must specify a PostgreSQL server.')

    database.setdefault('OPTIONS', {}).update(
        sslmode='verify-full',
        sslrootcert=certifi.where(),
    )
    return database


DATABASES = {'default': _database_config()}
# VA
