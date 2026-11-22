from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = (
            'customer_name',
            'customer_email',
            'customer_phone',
            'event_address',
            'event_at',
            'guest_count',
            'cuisine_type',
            'allergy_notes',
        )
