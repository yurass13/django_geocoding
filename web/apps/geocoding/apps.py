"""Geocoding apps"""
from django.apps import AppConfig


class GeocodingConfig(AppConfig):
    """Default AppConfig for Geocoding"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.geocoding'
