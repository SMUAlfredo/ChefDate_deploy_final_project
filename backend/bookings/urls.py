from django.urls import path

from .views import booking_csrf_token, create_booking

urlpatterns = [
    path('', create_booking, name='booking-create'),
    path('csrf/', booking_csrf_token, name='booking-csrf'),
]
