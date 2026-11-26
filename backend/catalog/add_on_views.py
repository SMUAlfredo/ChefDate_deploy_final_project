from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .add_ons import ADD_ONS


@require_GET
def list_add_ons(request):
    return JsonResponse(
        [
            {'slug': slug, 'name': service.name, 'price_cad': format(service.price_cad, '.2f')}
            for slug, service in ADD_ONS.items()
        ],
        safe=False,
    )
