"""Geocoding serializers"""
from rest_framework import serializers

from django.contrib.gis.geos import Point

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    """Default Address Serializer"""
    class Meta:
        model = Address
        fields = [
            'address',
            'postal_code',
            'country',
            'federal_district',
            'region_type',
            'region',
            'area_type',
            'area',
            'city_type',
            'city',
            'settlement_type',
            'settlement',
            'kladr_id',
            'fias_id',
            'fias_level',
            'capital_marker',
            'okato',
            'oktmo',
            'tax_office',
            'timezone',
            'geo_lat',
            'geo_lon',
            'population',
            'foundation_year'
        ]

    def create(self, validated_data):
        prototype = validated_data

        # location processing
        if prototype.get('geo_lat', None) is not None and prototype.get('geo_lon', None) is not None:
            prototype['location'] = Point(float(prototype['geo_lat']), float(prototype['geo_lon']))

        address = Address.objects.create(**prototype)
        return address
