from django.test import SimpleTestCase


class AddOnEndpointTests(SimpleTestCase):
    def test_lists_fixed_add_ons_and_prices(self):
        response = self.client.get('/api/catalog/add-ons/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'slug': 'cleaning', 'name': 'Cleaning', 'price_cad': '50.00'},
            {'slug': 'waitstaff', 'name': 'Waitstaff', 'price_cad': '80.00'},
        ])

    def test_rejects_post(self):
        response = self.client.post('/api/catalog/add-ons/')

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
