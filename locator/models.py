"""Database models for the locator application.

This module defines the Sanisette model representing public toilets in Paris
with their address, coordinates, accessibility, and other metadata.
"""

from __future__ import annotations

from django.db import models


class Sanisette(models.Model):
    """Model representing a public toilet (sanisette) in Paris."""

    type = models.CharField(max_length=50)
    adresse = models.CharField(max_length=255)
    complement_adresse = models.CharField(max_length=255, blank=True, null=True)
    arrondissement = models.CharField(max_length=5)
    horaire = models.CharField(max_length=100, blank=True, null=True)
    acces_pmr = models.CharField(max_length=10, blank=True, null=True)
    relais_bebe = models.CharField(max_length=10, blank=True, null=True)
    url_fiche_equipement = models.URLField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    gestionnaire = models.CharField(max_length=255, blank=True, null=True)
    source = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ("adresse", "latitude", "longitude")

    def __str__(self) -> str:
        """Return a human-readable representation of the sanisette."""
        return f"{self.adresse} ({self.arrondissement})"
