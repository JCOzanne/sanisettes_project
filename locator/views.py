from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from locator.models import Sanisette
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):

    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

class NearbySanisettesView(View):
    def get(self, request):
        try:
            lat = float(request.GET.get("lat"))
            lon = float(request.GET.get("lon"))
        except (TypeError, ValueError):
            return JsonResponse({"error": "Paramètres lat et lon requis."}, status=400)

        sanisettes = list(Sanisette.objects.all())

        sanisettes_with_distance = []
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
    template_name = "locator/map.html"
