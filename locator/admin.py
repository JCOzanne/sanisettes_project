"""Admin registrations for the locator app."""
from __future__ import annotations

from django.contrib import admin

from locator.models import Sanisette


@admin.register(Sanisette)
class SanisetteAdmin(admin.ModelAdmin):
    """Admin configuration for the Sanisette model."""

    list_display = ("adresse", "arrondissement", "horaire", "acces_pmr", "relais_bebe", "type")
    search_fields = ("adresse", "arrondissement")
    list_filter = ("arrondissement", "acces_pmr", "type")
