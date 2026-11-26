from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Chef, Cuisine


# Each cuisine includes three fictional chef profiles for the demo.
DEMO_CATALOG = (
    ('mexican', 'Mexican', (
        ('demo-marina-solano', 'Marina Solano', Decimal('145.00'), Decimal('4.7')),
        ('demo-tomas-rivera', 'Tomas Rivera', Decimal('170.00'), Decimal('4.9')),
        ('demo-elena-luna', 'Elena Luna', Decimal('155.00'), Decimal('4.6')),
    )),
    ('italian', 'Italian', (
        ('demo-lucia-monti', 'Lucia Monti', Decimal('180.00'), Decimal('4.8')),
        ('demo-matteo-serra', 'Matteo Serra', Decimal('160.00'), Decimal('4.5')),
        ('demo-silvia-riva', 'Silvia Riva', Decimal('195.00'), Decimal('4.9')),
    )),
    ('indian', 'Indian', (
        ('demo-mira-basu', 'Mira Basu', Decimal('150.00'), Decimal('4.7')),
        ('demo-arjun-kapoor', 'Arjun Kapoor', Decimal('175.00'), Decimal('4.8')),
        ('demo-neha-sen', 'Neha Sen', Decimal('165.00'), Decimal('4.6')),
    )),
    ('canadian', 'Canadian', (
        ('demo-avery-brooks', 'Avery Brooks', Decimal('165.00'), Decimal('4.7')),
        ('demo-morgan-ellis', 'Morgan Ellis', Decimal('185.00'), Decimal('4.9')),
        ('demo-rowan-bennett', 'Rowan Bennett', Decimal('150.00'), Decimal('4.5')),
    )),
    ('french', 'French', (
        ('demo-camille-renard', 'Camille Renard', Decimal('205.00'), Decimal('4.9')),
        ('demo-jules-martel', 'Jules Martel', Decimal('190.00'), Decimal('4.7')),
        ('demo-amelie-roux', 'Amelie Roux', Decimal('215.00'), Decimal('5.0')),
    )),
    ('spanish', 'Spanish', (
        ('demo-ines-vega', 'Ines Vega', Decimal('175.00'), Decimal('4.8')),
        ('demo-diego-salas', 'Diego Salas', Decimal('160.00'), Decimal('4.6')),
        ('demo-clara-ferrer', 'Clara Ferrer', Decimal('185.00'), Decimal('4.9')),
    )),
)


def _get_or_create_demo_record(model, slug, **fields):
    record, created = model.objects.get_or_create(slug=slug, defaults=fields)
    if not created and any(getattr(record, field) != value for field, value in fields.items()):
        raise CommandError(f'Demo {model._meta.verbose_name} slug conflict: {slug}.')
    return record, created


class Command(BaseCommand):
    help = 'Seed the demo catalog with six cuisines and eighteen fictional chefs.'

    def handle(self, *args, **options):
        cuisines_created = 0
        chefs_created = 0

        with transaction.atomic():
            for cuisine_slug, cuisine_name, chefs in DEMO_CATALOG:
                cuisine, created = _get_or_create_demo_record(Cuisine, cuisine_slug, name=cuisine_name)
                cuisines_created += created

                for slug, name, base_price_cad, rating in chefs:
                    _, created = _get_or_create_demo_record(
                        Chef,
                        slug,
                        name=name,
                        cuisine_id=cuisine.pk,
                        base_price_cad=base_price_cad,
                        rating=rating,
                    )
                    chefs_created += created

        self.stdout.write(self.style.SUCCESS(f'Created {cuisines_created} cuisines and {chefs_created} chefs.'))
