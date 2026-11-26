from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Cuisine, CuisinePhoto


CUISINE_SLUGS = ('canadian', 'french', 'indian', 'italian', 'mexican', 'spanish')
MAX_JPEG_BYTES = 5 * 1024 * 1024


def read_jpeg(path):
    try:
        with path.open('rb') as file:
            jpeg = file.read(MAX_JPEG_BYTES + 1)
    except OSError as error:
        raise CommandError(f'Could not read {path.name}.') from error

    if len(jpeg) > MAX_JPEG_BYTES or not (jpeg.startswith(b'\xff\xd8\xff') and jpeg.endswith(b'\xff\xd9')):
        raise CommandError(f'{path.name} must be a JPEG no larger than 5 MiB.')
    return jpeg


class Command(BaseCommand):
    help = 'Load the six demo JPEGs into the catalog photo table.'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=Path, help='Directory containing the slug-named JPEG files.')

    def handle(self, *args, directory, **options):
        photos = {slug: read_jpeg(directory / f'{slug}.jpg') for slug in CUISINE_SLUGS}
        created_count = 0

        with transaction.atomic():
            cuisines = Cuisine.objects.in_bulk(CUISINE_SLUGS, field_name='slug')
            missing = sorted(photos.keys() - cuisines.keys())
            if missing:
                raise CommandError(f'Missing cuisines: {", ".join(missing)}. Run seed_demo_catalog first.')

            for slug, jpeg in photos.items():
                photo, created = CuisinePhoto.objects.get_or_create(
                    cuisine=cuisines[slug], defaults={'jpeg': jpeg},
                )
                if not created and bytes(photo.jpeg) != jpeg:
                    raise CommandError(f'Demo photo conflict for {slug}.')
                created_count += created

        self.stdout.write(self.style.SUCCESS(f'Loaded {created_count} cuisine photos.'))
