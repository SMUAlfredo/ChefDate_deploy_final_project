from django.core.validators import MinValueValidator
from django.db import models


class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'


class Booking(models.Model):
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=32)
    event_address = models.CharField(max_length=255)
    event_at = models.DateTimeField('event date and time')
    guest_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cuisine_type = models.CharField(max_length=100)
    allergy_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=9,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(guest_count__gte=1),
                name='bookings_guest_count_at_least_one',
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=BookingStatus.values),
                name='bookings_status_valid',
            ),
        ]

    def __str__(self):
        return f'Booking #{self.pk}' if self.pk else 'New booking'
