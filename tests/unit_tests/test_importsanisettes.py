from unittest.mock import MagicMock, patch

import pytest
import requests
from django.core.management import call_command

from locator.models import Sanisette

API_URL = "https://data.ratp.fr/api/explore/v2.1/catalog/datasets/sanisettesparis2011/records"


@pytest.mark.django_db
class TestImportSanisettes:
    @patch("locator.management.commands.import_sanisettes.requests.get")
    def test_ignore_sanisette_without_coords(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = lambda: None
        mock_resp.text = "ok"
        mock_resp.json.side_effect = [
            {"results": [{"adresse": "Rue Test", "geo_point_2d": None, "arrondissement": "75001"}]},
            {"results": []},
        ]
        mock_get.return_value = mock_resp

        call_command("import_sanisettes")
        assert Sanisette.objects.count() == 0

    @patch("locator.management.commands.import_sanisettes.requests.get")
    def test_accept_sanisette_with_missing_address(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = lambda: None
        mock_resp.text = "ok"
        mock_resp.json.side_effect = [
            {"results": [{"adresse": None, "geo_point_2d": {"lat": 48.85, "lon": 2.35}, "arrondissement": "75001"}]},
            {"results": []},
        ]
        mock_get.return_value = mock_resp

        call_command("import_sanisettes")
        assert Sanisette.objects.count() == 0

    @patch("locator.management.commands.import_sanisettes.requests.get")
    def test_idempotency_no_duplicates_on_second_run(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = lambda: None
        mock_resp.text = "ok"
        mock_resp.json.side_effect = [
            {
                "results": [
                    {"adresse": "Rue Test", "geo_point_2d": {"lat": 48.85, "lon": 2.35}, "arrondissement": "75001"}
                ]
            },
            {"results": []},
        ]
        mock_get.return_value = mock_resp

        call_command("import_sanisettes")

        mock_resp.json.side_effect = [
            {
                "results": [
                    {"adresse": "Rue Test", "geo_point_2d": {"lat": 48.85, "lon": 2.35}, "arrondissement": "75001"}
                ]
            },
            {"results": []},
        ]
        call_command("import_sanisettes")

        assert Sanisette.objects.count() == 1

    @patch("locator.management.commands.import_sanisettes.requests.get")
    def test_api_failure_is_handled(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("API down")

        with pytest.raises(requests.exceptions.RequestException):
            call_command("import_sanisettes")
