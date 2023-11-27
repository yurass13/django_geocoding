from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
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
            'foundation_year',
        ]
