"""Geocoding validators"""
from datetime import datetime

from typing import Optional

from django.core.validators import ValidationError


def validate_foundation_year(value: Optional[str | int]) -> Optional[int]:
    """
    :param value: int | str - foundation year.
    :returns int: value is valid
    :return None: value is None.
    :raise ValidationError: int(value) > datetime.now().year or int(value) < -10000
    """
    if value is None:
        return value

    try:
        value = int(value)

        if value > datetime.now().year:
            raise ValueError("Expected a year of foundation, but value is too big!")

        if value < -10000:
            raise ValueError("Expected a year of foundation, but value is too small!")

        return value
    except ValueError as error:
        raise ValidationError(f"Expected a year of foundation, but got {value}:{type(value)}!") from error


def validate_population(value: Optional[str | int]) -> Optional[int]:
    """
    :param value: int | str - population count.
    :returns int: value is valid.
    :return None: value is None.
    :raises ValidationError: value < 0 or value > 7_000_000_000
    """
    if value is None:
        return value

    try:
        value = int(value)

        if value > 7_000_000_000:
            raise ValueError("Expected population in the region, but the value is too big!")

        if value < 0:
            raise ValueError("Expected population in the region, but the value is too small!")

        return value
    except ValueError as error:
        raise ValidationError(f"Expected population in the region, but got {value}:{type(value)}!") from error
