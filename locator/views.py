"""Views for the locator application.

Provides an endpoint to retrieve the nearest sanisettes and a simple map page.
"""
from __future__ import annotations

from math import asin, cos, radians, sin, sqrt
from typing import List, Tuple

from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.generic import TemplateView

from locator.models import Sanisette


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute the great-circle distance between two points on Earth in km.

    Uses the haversine formula. Inputs are decimal degrees.
    """

    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


class NearbySanisettesView(View):
    """Return the five nearest sanisettes to a lat/lon query via JSON."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Handle GET requests.

        Expects query parameters lat and lon as floats.
        Returns a JSON array of up to five sanisettes sorted by distance.
        """
        try:
            lat = float(request.GET.get("lat"))
            lon = float(request.GET.get("lon"))
        except (TypeError, ValueError):
            return JsonResponse({"error": "Paramètres lat et lon requis."}, status=400)

        sanisettes: List[Sanisette] = list(Sanisette.objects.all())

        sanisettes_with_distance: List[Tuple[float, Sanisette]] = []
        for s in sanisettes:
            if s.latitude and s.longitude:
                distance = haversine(lat, lon, s.latitude, s.longitude)
                sanisettes_with_distance.append((distance, s))

        sanisettes_with_distance.sort(key=lambda x: x[0])
        nearest = sanisettes_with_distance[:5]

        data = [
            {
                "adresse": s.adresse,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "distance_km": round(d, 3),
                "acces_pmr": s.acces_pmr,
                "horaire": s.horaire,
            }
            for d, s in nearest
        ]

        return JsonResponse(data, safe=False)


class MapView(TemplateView):
    """Render the interactive map page."""

    template_name = "locator/map.html"
