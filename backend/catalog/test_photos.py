from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import CommandError, call_command
from django.test import TestCase

from .models import Cuisine, CuisinePhoto


class CuisinePhotoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo_catalog', stdout=StringIO())

    def test_loader_is_repeatable_and_photo_is_served_as_jpeg(self):
        photos = self.write_photo_fixtures()
        first = StringIO()
        second = StringIO()
        call_command('load_cuisine_photos', photos, stdout=first)
        call_command('load_cuisine_photos', photos, stdout=second)

        self.assertIn('Loaded 6 cuisine photos.', first.getvalue())
        self.assertIn('Loaded 0 cuisine photos.', second.getvalue())
        self.assertEqual(CuisinePhoto.objects.count(), 6)

        response = self.client.get('/api/catalog/photos/mexican/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/jpeg')
        self.assertEqual(response.content, (photos / 'mexican.jpg').read_bytes())
        self.assertEqual(self.client.get('/api/catalog/photos/unknown/').status_code, 404)
        self.assertEqual(self.client.post('/api/catalog/photos/mexican/').status_code, 405)

    def test_conflicting_photo_rolls_back_earlier_inserts(self):
        photos = self.write_photo_fixtures()
        existing = CuisinePhoto.objects.create(cuisine=Cuisine.objects.get(slug='spanish'), jpeg=b'existing')

        with self.assertRaisesMessage(CommandError, 'Demo photo conflict for spanish.'):
            call_command('load_cuisine_photos', photos, stdout=StringIO())

        self.assertEqual(list(CuisinePhoto.objects.values_list('pk', flat=True)), [existing.pk])

    def write_photo_fixtures(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name)
        for slug in Cuisine.objects.values_list('slug', flat=True):
            (path / f'{slug}.jpg').write_bytes(b'\xff\xd8\xff' + slug.encode('ascii') + b'\xff\xd9')
        return path
