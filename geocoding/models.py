from django.db import models
from django.contrib.auth.models import User
from .validators import validate_foundation_year, validate_population


class Address(models.Model):

    class FiasLevel(models.Choices):
        COUNTRY = 0
        REGION = 1
        AREA = 3
        CITY = 4
        CITY_AREA = 5
        LOCALITY = 6
        STREET = 7
        HOUSE = 8
        APARTMENT = 9
        STRUCT = 65
        ADDITIONAL_TERRITORY = 90
        ADDITIONAL_TER_STREET = 91
        FOREIGN_OR_EMPTY = -1

    class CapitalMarker(models.Choices):
        OTHER = 0
        AREA_CENTER = 1
        REGION_CENTER = 2
        REGION_AREA_CENTER = 3
        CENTRAL_AREA = 4

    address = models.CharField(max_length=500)
    postal_code = models.CharField(max_length=6, blank=True)
    country = models.CharField(max_length=120)
    federal_district = models.CharField(max_length=20)
    region_type = models.CharField(max_length=10)
    region = models.CharField(max_length=120)
    area_type = models.CharField(max_length=10, blank=True)
    area = models.CharField(max_length=255, blank=True)
    city_type = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=120, blank=True)
    settlement_type = models.CharField(max_length=10, blank=True)
    settlement = models.CharField(max_length=120, blank=True)
    kladr_id = models.CharField(max_length=19)
    fias_id = models.CharField(max_length=36, unique=True)
    fias_level = models.IntegerField(choices=FiasLevel.choices,
                                     default=FiasLevel.FOREIGN_OR_EMPTY)
    capital_marker = models.IntegerField(choices=CapitalMarker.choices,
                                         default=CapitalMarker.OTHER)
    okato = models.CharField(max_length=11, blank=True)
    oktmo = models.CharField(max_length=11, blank=True)
    tax_office = models.CharField(max_length=4, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    geo_lat = models.FloatField(max_length=12)
    geo_lon = models.FloatField(max_length=12)
    population = models.IntegerField(default=0,
                                     validators=[
                                         validate_population
                                     ])
    foundation_year = models.IntegerField(null=True,
                                          default=None,
                                          validators=[
                                              validate_foundation_year
                                          ])

    class Meta:
        indexes = [
            models.Index(fields=['postal_code']),
            models.Index(fields=['country']),
            models.Index(fields=['city']),
            models.Index(fields=['kladr_id']),
            models.Index(fields=['fias_id']),
            models.Index(fields=['okato']),
            models.Index(fields=['oktmo']),
            models.Index(fields=['geo_lat']),
            models.Index(fields=['geo_lon'])
        ]

    def __str__(self):
        return self.address
