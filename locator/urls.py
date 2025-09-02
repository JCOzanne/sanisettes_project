"""URL routes for the locator app."""
from __future__ import annotations

from django.urls import path

from .views import MapView, NearbySanisettesView

urlpatterns = [
    path("map/", MapView.as_view(), name="map"),
    path("api/nearby-sanisettes/", NearbySanisettesView.as_view(), name="nearby_sanisettes"),
]
