from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .models import Chef, Cuisine


class CatalogEndpointTests(TestCase):
    def test_empty_catalog_returns_an_empty_list(self):
        response = self.client.get('/api/catalog/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_seeded_catalog_returns_sorted_cuisines_and_chefs(self):
        call_command('seed_demo_catalog', stdout=StringIO())

        response = self.client.get('/api/catalog/')

        self.assertEqual(response.status_code, 200)
        catalog = response.json()
        self.assertEqual(
            [(cuisine['slug'], cuisine['name']) for cuisine in catalog],
            [
                ('canadian', 'Canadian'),
                ('french', 'French'),
                ('indian', 'Indian'),
                ('italian', 'Italian'),
                ('mexican', 'Mexican'),
                ('spanish', 'Spanish'),
            ],
        )
        for cuisine in catalog:
            self.assertEqual(set(cuisine), {'slug', 'name', 'chefs'})
            chef_slugs = [chef['slug'] for chef in cuisine['chefs']]
            self.assertEqual(len(chef_slugs), 3)
            self.assertEqual(chef_slugs, sorted(chef_slugs))
            for chef in cuisine['chefs']:
                self.assertEqual(set(chef), {'slug', 'name', 'base_price_cad', 'rating'})
                self.assertRegex(chef['base_price_cad'], r'^\d+\.\d{2}$')
        self.assertEqual(
            catalog[0]['chefs'][0],
            {
                'slug': 'demo-avery-brooks',
                'name': 'Avery Brooks',
                'base_price_cad': '165.00',
                'rating': 4.7,
            },
        )

    def test_post_is_rejected_without_writing_records(self):
        response = self.client.post('/api/catalog/', {'name': 'Unexpected cuisine'})

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        self.assertFalse(Cuisine.objects.exists())
        self.assertFalse(Chef.objects.exists())
