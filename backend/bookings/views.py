import json

from django.conf import settings
from django.http import JsonResponse
from django.http.request import UnreadablePostError
from django.middleware.csrf import get_token
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from .forms import BookingForm

MAX_BOOKING_BODY_BYTES = 32 * 1024


@require_GET
@never_cache
def booking_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


@require_POST
def create_booking(request):
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'expected_json'}, status=400)

    max_bytes = MAX_BOOKING_BODY_BYTES
    if settings.DATA_UPLOAD_MAX_MEMORY_SIZE is not None:
        max_bytes = min(max_bytes, settings.DATA_UPLOAD_MAX_MEMORY_SIZE)

    try:
        body = request.read(max_bytes + 1)
    except UnreadablePostError:
        return JsonResponse({'error': 'invalid_json'}, status=400)

    if len(body) > max_bytes:
        return JsonResponse({'error': 'request_too_large'}, status=413)

    try:
        data = json.loads(body)
    except (ValueError, RecursionError):
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
