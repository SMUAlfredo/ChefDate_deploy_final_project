from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from .models import CuisinePhoto


@require_GET
def cuisine_photo(request, slug):
    jpeg = get_object_or_404(
        CuisinePhoto.objects.values_list('jpeg', flat=True),
        cuisine__slug=slug,
    )
    return HttpResponse(bytes(jpeg), content_type='image/jpeg')
