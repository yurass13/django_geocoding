"""Map apps"""
from django.apps import AppConfig


class MapConfig(AppConfig):
    """Base Map App Config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.map'
