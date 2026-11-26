from django.urls import path

from .photo_views import cuisine_photo
from .views import list_catalog

urlpatterns = [
    path('', list_catalog, name='catalog-list'),
    path('photos/<slug:slug>/', cuisine_photo, name='cuisine-photo'),
]
