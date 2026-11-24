import json

from django.core.exceptions import RequestDataTooBig
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from .forms import BookingForm


@require_GET
@never_cache
def booking_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


@require_POST
def create_booking(request):
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'expected_json'}, status=400)

    try:
        data = json.loads(request.body)
    except (ValueError, RecursionError, RequestDataTooBig):
        return JsonResponse({'error': 'invalid_json'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'error': 'expected_json_object'}, status=400)

    form = BookingForm(data)
    errors = form.json_field_errors()
    if errors:
        return JsonResponse({'errors': errors}, status=400)

    if not form.is_valid():
        return JsonResponse({'errors': form.error_codes()}, status=400)

    booking = form.save()
    return JsonResponse({'id': booking.pk}, status=201)
# VA
