from django.urls import path

from .views import list_catalog

urlpatterns = [
    path('', list_catalog, name='catalog-list'),
]
