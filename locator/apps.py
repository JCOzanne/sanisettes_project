"""Django application configuration for the locator app."""

from __future__ import annotations

from django.apps import AppConfig


class LocatorConfig(AppConfig):
    """AppConfig for the locator application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "locator"
