import re
from datetime import timezone

from django import forms

from catalog.models import Chef

from .models import Booking


class BookingForm(forms.ModelForm):
    allergy_notes = forms.CharField(required=False, max_length=1000, widget=forms.Textarea)
    preferred_chef_slug = forms.SlugField(required=False, max_length=50)

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

    def clean_preferred_chef_slug(self):
        slug = self.cleaned_data['preferred_chef_slug']
        if not slug and 'preferred_chef_slug' in self.data:
            raise forms.ValidationError('Enter a chef slug.', code='invalid')
        return slug

    def clean(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get('preferred_chef_slug')
        cuisine_name = cleaned_data.get('cuisine_type')
        if not slug or not cuisine_name:
            return cleaned_data

        try:
            chef = Chef.objects.select_related('cuisine').get(slug=slug)
        except Chef.DoesNotExist:
            self.add_error('preferred_chef_slug', forms.ValidationError('Unknown chef.', code='unknown_chef'))
            return cleaned_data

        if chef.cuisine.name.casefold() != cuisine_name.casefold():
            self.add_error(
                'preferred_chef_slug',
                forms.ValidationError('Choose a chef for the preferred cuisine.', code='cuisine_mismatch'),
            )
        else:
            self.instance.preferred_chef = chef
        return cleaned_data

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
