import re
from datetime import timezone

from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    allergy_notes = forms.CharField(required=False, max_length=1000, widget=forms.Textarea)

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

    def clean_event_at(self):
        try:
            return self.cleaned_data['event_at'].astimezone(timezone.utc)
        except OverflowError:
            message = self.fields['event_at'].error_messages['invalid']
            raise forms.ValidationError(message, code='invalid') from None

    def json_field_errors(self):
        errors = {}
        for field in self.fields:
            if field not in self.data:
                continue

            value = self.data[field]
            expected_type = int if field == 'guest_count' else str
            if type(value) is not expected_type:
                errors[field] = ['invalid_type']
            elif isinstance(value, str) and re.search(r'[\ud800-\udfff]', value):
                errors[field] = ['invalid']
        return errors

    def error_codes(self):
        return {
            field: [error.code for error in errors]
            for field, errors in self.errors.as_data().items()
        }
# VA
