from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Chef, Cuisine


@require_GET
def list_catalog(request):
    cuisines = Cuisine.objects.order_by('slug').prefetch_related(
        Prefetch('chef_set', queryset=Chef.objects.order_by('slug')),
    )
    catalog = [
        {
            'slug': cuisine.slug,
            'name': cuisine.name,
            'chefs': [
                {
                    'slug': chef.slug,
                    'name': chef.name,
                    'base_price_cad': format(chef.base_price_cad, '.2f'),
                    'rating': float(chef.rating),
                }
                for chef in cuisine.chef_set.all()
            ],
        }
        for cuisine in cuisines
    ]
    return JsonResponse(catalog, safe=False)
