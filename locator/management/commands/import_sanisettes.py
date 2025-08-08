import requests
from django.core.management.base import BaseCommand
from locator.models import Sanisette

API_URL = "https://data.ratp.fr/api/explore/v2.1/catalog/datasets/sanisettesparis2011/records"
LIMIT = 100

class Command(BaseCommand):
    help = "Importe les sanisettes de Paris depuis l’API RATP"

    def handle(self, *args, **kwargs):
        self.stdout.write("Import des sanisettes en cours...")

        offset = 0
        total_imported = 0

        while True:
            params = {
                "limit": LIMIT,
                "offset": offset
            }

            response = requests.get(API_URL, params=params)
            data = response.json()

            results = data.get("results", [])
            if not results:
                break

            for item in results:
                coords = item.get("geo_point_2d")
                if not isinstance(coords, dict):
                    continue

                lat = coords.get("lat")
                lon = coords.get("lon")

                if lat is None or lon is None:
                    continue

                adresse = item.get("adresse")
                if not adresse:
                    continue

                sanisette, created = Sanisette.objects.update_or_create(
                    adresse=adresse,
                    defaults={
                        "type": item.get("type", ""),
                        "complement_adresse": item.get("complement_adresse"),
                        "arrondissement": item.get("arrondissement"),
                        "horaire": item.get("horaire"),
                        "acces_pmr": item.get("acces_pmr"),
                        "relais_bebe": item.get("relais_bebe"),
                        "url_fiche_equipement": item.get("url_fiche_equipement"),
                        "latitude": lat,
                        "longitude": lon,
                        "gestionnaire": item.get("gestionnaire"),
                        "source": item.get("source"),
                    }
                )
                total_imported += 1

            offset += LIMIT

        self.stdout.write(self.style.SUCCESS(f"{total_imported} sanisettes importées avec succès."))
