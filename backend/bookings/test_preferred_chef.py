from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Chef, Cuisine

from .models import Booking, BookingStatus


class PreferredChefBookingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cuisine = Cuisine.objects.create(slug='mexican', name='Mexican')
        cls.chef = Chef.objects.create(
            slug='demo-sample-chef',
            name='Sample Chef',
            cuisine=cuisine,
            base_price_cad=Decimal('120.00'),
            rating=Decimal('4.5'),
        )

    def post_booking(self, **changes):
        payload = {
            'customer_name': 'Sample Guest',
            'customer_email': 'guest@example.test',
            'customer_phone': '902-555-0101',
            'event_address': '1 Sample Street',
            'event_at': '2027-05-28T18:00:00Z',
            'guest_count': 3,
            'cuisine_type': 'Mexican',
        }
        return self.client.post(reverse('booking-create'), payload | changes, content_type='application/json')

    def test_matching_chef_is_saved_on_a_pending_booking(self):
        response = self.post_booking(preferred_chef_slug=self.chef.slug, status=BookingStatus.CONFIRMED)

        self.assertEqual(response.status_code, 201)
        booking = Booking.objects.get()
        self.assertEqual(response.json(), {'id': booking.pk})
        self.assertEqual(booking.cuisine_type, 'Mexican')
        self.assertEqual(booking.preferred_chef, self.chef)
        self.assertEqual(booking.status, BookingStatus.PENDING)

    def test_unknown_or_mismatched_chef_does_not_create_a_booking(self):
        cases = (
            ('unknown-chef', 'Mexican', 'unknown_chef'),
            (self.chef.slug, 'Italian', 'cuisine_mismatch'),
        )
        for slug, cuisine, code in cases:
            with self.subTest(slug=slug, cuisine=cuisine):
                response = self.post_booking(preferred_chef_slug=slug, cuisine_type=cuisine)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json(), {'errors': {'preferred_chef_slug': [code]}})
                self.assertFalse(Booking.objects.exists())

    def test_invalid_slug_values_are_rejected(self):
        for slug, code in (('', 'invalid'), ('bad slug', 'invalid'), (None, 'invalid_type')):
            with self.subTest(slug=slug):
                response = self.post_booking(preferred_chef_slug=slug)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json(), {'errors': {'preferred_chef_slug': [code]}})
                self.assertFalse(Booking.objects.exists())

    def test_omitting_preference_accepts_existing_cuisine_text(self):
        response = self.post_booking(cuisine_type='Family-style menu')

        self.assertEqual(response.status_code, 201)
        booking = Booking.objects.get()
        self.assertEqual(response.json(), {'id': booking.pk})
        self.assertEqual(booking.cuisine_type, 'Family-style menu')
        self.assertIsNone(booking.preferred_chef_id)
        self.assertEqual(booking.status, BookingStatus.PENDING)
