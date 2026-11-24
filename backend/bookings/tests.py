from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import connection
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.html import escape

from .models import Booking, BookingStatus


class BookingCreationTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        csrf = self.client.get(reverse('booking-csrf'))
        self.assertEqual(csrf.status_code, 200)
        self.assertIn('no-store', csrf['Cache-Control'])
        self.assertIn('csrftoken', csrf.cookies)
        self.csrf_headers = {'X-CSRFToken': csrf.json()['csrfToken']}
        self.url = reverse('booking-create')
        self.payload = {
            'customer_name': 'Synthetic ChefDate Guest',
            'customer_email': 'guest@example.invalid',
            'customer_phone': '+1 902 555 0100',
            'event_address': '42 Example Street',
            'event_at': '2030-07-14T19:30:00-03:00',
            'guest_count': 6,
            'cuisine_type': 'Italian',
        }

    def post_booking(self, payload):
        return self.client.post(
            self.url,
            payload,
            content_type='application/json',
            headers=self.csrf_headers,
        )

    def test_valid_booking_is_pending_and_visible_in_admin(self):
        response = self.post_booking({**self.payload, 'id': 999, 'status': 'confirmed'})

        booking = Booking.objects.get()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': booking.pk})
        self.assertNotEqual(booking.pk, 999)
        self.assertEqual(booking.status, BookingStatus.PENDING)
        self.assertEqual(booking.allergy_notes, '')
        self.assertEqual(booking.event_at, datetime(2030, 7, 14, 22, 30, tzinfo=timezone.utc))

        admin_url = reverse('admin:bookings_booking_changelist')
        self.assertEqual(self.client.get(admin_url).status_code, 302)
        staff = get_user_model().objects.create_user(username='staff-test', is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(admin_url).status_code, 403)
        administrator = get_user_model().objects.create_superuser(username='admin-test')
        self.client.force_login(administrator)
        page = self.client.get(admin_url)
        self.assertContains(page, booking.customer_name)
        self.assertContains(page, 'Pending')
        self.assertNotContains(page, booking.customer_email)

    def test_optional_allergy_notes_are_saved_without_appearing_in_response(self):
        notes = 'Synthetic allergy notes'
        response = self.post_booking({**self.payload, 'allergy_notes': notes})

        booking = Booking.objects.get()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': booking.pk})
        self.assertEqual(booking.allergy_notes, notes)

    def test_booking_insert_binds_customer_data_and_admin_escapes_it(self):
        name = "O'Neil & <Chef>"
        inserts = []

        def capture_insert(execute, sql, params, many, context):
            if sql.lstrip().upper().startswith('INSERT'):
                inserts.append((sql, params))
            return execute(sql, params, many, context)

        with connection.execute_wrapper(capture_insert):
            response = self.post_booking({**self.payload, 'customer_name': name})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.get().customer_name, name)
        self.assertEqual(len(inserts), 1)
        sql, params = inserts[0]
        self.assertNotIn(name, sql)
        self.assertIn(name, params)

        administrator = get_user_model().objects.create_superuser(username='escaping-admin')
        self.client.force_login(administrator)
        page = self.client.get(reverse('admin:bookings_booking_changelist'))
        self.assertContains(page, escape(name))
        self.assertNotContains(page, name)

    def test_admin_view_permission_does_not_allow_booking_changes(self):
        self.assertEqual(self.post_booking(self.payload).status_code, 201)
        booking = Booking.objects.get()
        staff = get_user_model().objects.create_user(username='view-only', is_staff=True)
        staff.user_permissions.add(
            Permission.objects.get(content_type__app_label='bookings', codename='view_booking')
        )
        self.client.force_login(staff)

        change_url = reverse('admin:bookings_booking_change', args=[booking.pk])
        self.assertEqual(self.client.get(change_url).status_code, 200)
        csrf = self.client.get(reverse('booking-csrf')).json()['csrfToken']
        response = self.client.post(
            change_url, {'status': BookingStatus.CONFIRMED}, headers={'X-CSRFToken': csrf},
        )
        self.assertEqual(response.status_code, 403)
        booking.refresh_from_db()
        self.assertEqual(booking.status, BookingStatus.PENDING)

    def test_allergy_notes_accept_the_limit_and_reject_longer_values(self):
        notes = 'a' * 1000
        response = self.post_booking({**self.payload, 'allergy_notes': notes})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.get().allergy_notes, notes)

        response = self.post_booking({**self.payload, 'allergy_notes': notes + 'a'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'errors': {'allergy_notes': ['max_length']}})
        self.assertEqual(Booking.objects.count(), 1)

    def test_large_request_is_rejected_before_decoding(self):
        response = self.post_booking(' ' * (32 * 1024 + 1))

        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.json(), {'error': 'request_too_large'})
        self.assertFalse(Booking.objects.exists())

    def test_missing_required_field_does_not_save(self):
        del self.payload['event_address']
        response = self.post_booking(self.payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'errors': {'event_address': ['required']}})
        self.assertFalse(Booking.objects.exists())

    def test_model_validation_rejects_invalid_values(self):
        for field, value in (
            ('customer_email', 'not-an-email'),
            ('event_at', 'not-a-date'),
            ('event_at', '9999-12-31T23:59:59-01:00'),
            ('guest_count', 0),
        ):
            with self.subTest(field=field):
                response = self.post_booking({**self.payload, field: value})
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json()['errors'])
                self.assertFalse(Booking.objects.exists())

    def test_malformed_json_and_invalid_value_types_do_not_save(self):
        for payload in (
            '{',
            '[]',
            {**self.payload, 'guest_count': True},
            {**self.payload, 'customer_name': '\ud800'},
        ):
            with self.subTest(payload=payload):
                self.assertEqual(self.post_booking(payload).status_code, 400)
        self.assertFalse(Booking.objects.exists())

    def test_csrf_and_post_only_protections(self):
        response = self.client.post(self.url, self.payload, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        cross_origin = self.client.post(
            self.url,
            self.payload,
            content_type='application/json',
            headers={**self.csrf_headers, 'Origin': 'https://example.invalid'},
        )
        self.assertEqual(cross_origin.status_code, 403)
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.assertFalse(Booking.objects.exists())
# VA
