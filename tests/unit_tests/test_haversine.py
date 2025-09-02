import pytest

from locator.views import haversine


def test_haversine_zero_distance():
    lat, lon = 48.8566, 2.3522
    distance = haversine(lat, lon, lat, lon)
    assert distance == pytest.approx(0, abs=1e-6)


def test_haversine_known_distance():
    dist = haversine(48.8566, 2.3522, 51.5074, -0.1278)
    assert dist == pytest.approx(343, abs=5)
