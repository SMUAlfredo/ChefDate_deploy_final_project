from django.urls import path

from .add_on_views import list_add_ons
from .photo_views import cuisine_photo
from .views import list_catalog

urlpatterns = [
    path('', list_catalog, name='catalog-list'),
    path('add-ons/', list_add_ons, name='catalog-add-ons'),
    path('photos/<slug:slug>/', cuisine_photo, name='cuisine-photo'),
]
