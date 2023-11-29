from django.contrib.gis.db import models
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
    postal_code = models.CharField(max_length=6, null=True, default=None)
    country = models.CharField(max_length=120)
    federal_district = models.CharField(max_length=20)
    region_type = models.CharField(max_length=10)
    region = models.CharField(max_length=120)
    area_type = models.CharField(max_length=10, null=True, default=None)
    area = models.CharField(max_length=255, null=True, default=None)
    city_type = models.CharField(max_length=10, null=True, default=None)
    city = models.CharField(max_length=120, null=True, default=None)
    settlement_type = models.CharField(max_length=10, null=True, default=None)
    settlement = models.CharField(max_length=120, null=True, default=None)
    kladr_id = models.CharField(max_length=19)
    fias_id = models.CharField(max_length=36, unique=True)
    fias_level = models.IntegerField(choices=FiasLevel.choices,
                                     default=FiasLevel.FOREIGN_OR_EMPTY)
    capital_marker = models.IntegerField(choices=CapitalMarker.choices,
                                         default=CapitalMarker.OTHER)
    okato = models.CharField(max_length=11, null=True, default=None)
    oktmo = models.CharField(max_length=11, null=True, default=None)
    tax_office = models.CharField(max_length=4, null=True, default=None)
    timezone = models.CharField(max_length=50, null=True, default=None)
    geo_lat = models.FloatField(max_length=12)
    geo_lon = models.FloatField(max_length=12)
    population = models.BigIntegerField(null=True,
                                        default=None,
                                        validators=[
                                             validate_population
                                        ])
    foundation_year = models.IntegerField(null=True,
                                          default=None,
                                          validators=[
                                              validate_foundation_year
                                          ])
    location = models.PointField(null=True, default=None, srid=4326)

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
