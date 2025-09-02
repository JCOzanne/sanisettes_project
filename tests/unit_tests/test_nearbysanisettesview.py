from unittest.mock import patch

import pytest
from django.urls import reverse

from locator.models import Sanisette


@pytest.mark.django_db
class TestNearbySanisettesView:

    @pytest.fixture(autouse=True)
    def setup_data(self):
        Sanisette.objects.create(adresse="1 Rue A", latitude=48.8566, longitude=2.3522, acces_pmr=True, horaire="24/7")
        Sanisette.objects.create(
            adresse="2 Rue B", latitude=48.8567, longitude=2.3530, acces_pmr=False, horaire="8h-20h"
        )
        Sanisette.objects.create(
            adresse="3 Rue C", latitude=48.8570, longitude=2.3540, acces_pmr=True, horaire="9h-18h"
        )

    def test_view_returns_5_or_less_sanisettes(self, client):
        url = reverse("nearby_sanisettes")
        response = client.get(url, {"lat": "48.8566", "lon": "2.3522"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
        assert "adresse" in data[0]
        assert "distance_km" in data[0]

    def test_view_missing_params(self, client):
        url = reverse("nearby_sanisettes")
        response = client.get(url)
        assert response.status_code == 400
        assert "error" in response.json()

    def test_view_invalid_params(self, client):
        url = reverse("nearby_sanisettes")
        response = client.get(url, {"lat": "abc", "lon": "def"})
        assert response.status_code == 400
        assert "error" in response.json()


@pytest.mark.django_db
class TestNearbySanisettesExtra:

    def test_returns_less_than_5_if_db_smaller(self, client):
        Sanisette.objects.create(adresse="1", latitude=48.85, longitude=2.35)
        Sanisette.objects.create(adresse="2", latitude=48.86, longitude=2.36)

        url = reverse("nearby_sanisettes") + "?lat=48.85&lon=2.35"
        response = client.get(url)
        data = response.json()

        assert len(data) == 2
        assert all("distance_km" in s for s in data)

    @patch("locator.views.Sanisette.objects.all")
    def test_ignores_sanisettes_without_coords(self, mock_all, client):
        class FakeSanisette:
            def __init__(self, adresse, latitude, longitude):
                self.adresse = adresse
                self.latitude = latitude
                self.longitude = longitude
                self.acces_pmr = True
                self.horaire = "24/7"

        mock_all.return_value = [
            FakeSanisette("Sans coords", None, None),
            FakeSanisette("Avec coords", 48.85, 2.35),
        ]

        url = reverse("nearby_sanisettes") + "?lat=48.85&lon=2.35"
        response = client.get(url)
        data = response.json()

        assert len(data) == 1
        assert data[0]["adresse"] == "Avec coords"
