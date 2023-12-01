# Generated by Django 4.2.7 on 2023-11-29 07:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models
from apps.geocoding import validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geocoding', '0000_postgis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500)),
                ('postal_code', models.CharField(default=None, max_length=6, null=True)),
                ('country', models.CharField(max_length=120)),
                ('federal_district', models.CharField(max_length=20)),
                ('region_type', models.CharField(max_length=10)),
                ('region', models.CharField(max_length=120)),
                ('area_type', models.CharField(default=None, max_length=10, null=True)),
                ('area', models.CharField(default=None, max_length=255, null=True)),
                ('city_type', models.CharField(default=None, max_length=10, null=True)),
                ('city', models.CharField(default=None, max_length=120, null=True)),
                ('settlement_type', models.CharField(default=None, max_length=10, null=True)),
                ('settlement', models.CharField(default=None, max_length=120, null=True)),
                ('kladr_id', models.CharField(max_length=19)),
                ('fias_id', models.CharField(max_length=36, unique=True)),
                ('fias_level', models.IntegerField(choices=[(0, 'Country'),
                                                            (1, 'Region'),
                                                            (3, 'Area'),
                                                            (4, 'City'),
                                                            (5, 'City Area'),
                                                            (6, 'Locality'),
                                                            (7, 'Street'),
                                                            (8, 'House'),
                                                            (9, 'Apartment'),
                                                            (65, 'Struct'),
                                                            (90, 'Additional Territory'),
                                                            (91, 'Additional Ter Street'),
                                                            (-1, 'Foreign Or Empty')],
                                                   default=-1)),
                ('capital_marker', models.IntegerField(choices=[(0, 'Other'),
                                                                (1, 'Area Center'),
                                                                (2, 'Region Center'),
                                                                (3, 'Region Area Center'),
                                                                (4, 'Central Area')],
                                                       default=0)),
                ('okato', models.CharField(default=None, max_length=11, null=True)),
                ('oktmo', models.CharField(default=None, max_length=11, null=True)),
                ('tax_office', models.CharField(default=None, max_length=4, null=True)),
                ('timezone', models.CharField(default=None, max_length=50, null=True)),
                ('geo_lat', models.FloatField(max_length=12)),
                ('geo_lon', models.FloatField(max_length=12)),
                ('population', models.BigIntegerField(default=None,
                                                      null=True,
                                                      validators=[validators.validate_population])),
                ('foundation_year', models.IntegerField(default=None,
                                                        null=True,
                                                        validators=[validators.validate_foundation_year])),
                ('location', django.contrib.gis.db.models.fields.PointField(default=None, null=True, srid=4326)),
            ],
            options={
                'indexes': [models.Index(fields=['postal_code'], name='geocoding_a_postal__3f7ec3_idx'),
                            models.Index(fields=['country'], name='geocoding_a_country_390423_idx'),
                            models.Index(fields=['city'], name='geocoding_a_city_4fe345_idx'),
                            models.Index(fields=['kladr_id'], name='geocoding_a_kladr_i_54cc3e_idx'),
                            models.Index(fields=['fias_id'], name='geocoding_a_fias_id_507537_idx'),
                            models.Index(fields=['okato'], name='geocoding_a_okato_b9b725_idx'),
                            models.Index(fields=['oktmo'], name='geocoding_a_oktmo_a5a549_idx'),
                            models.Index(fields=['geo_lat'], name='geocoding_a_geo_lat_faa0de_idx'),
                            models.Index(fields=['geo_lon'], name='geocoding_a_geo_lon_79c460_idx')],
            },
        ),
    ]