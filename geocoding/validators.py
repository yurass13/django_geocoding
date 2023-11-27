from django.core.validators import ValidationError
from datetime import datetime


def validate_foundation_year(value: str | int) -> int:
    try:
        value = int(value)

        if value > datetime.now().year:
            raise ValueError("Expected a year of foundation, but value is too big!")

        if value < -10000:
            raise ValueError("Expected a year of foundation, but value is too small!")

        return value
    except ValueError:
        raise ValidationError(f"Expected a year of foundation, but got {value}:{type(value)}!")


def validate_population(value: str | int) -> int:
    try:
        value = int(value)

        if value > 7_000_000_000:
            raise ValueError("Expected population in the region, but the value is too big!")

        if value < 0:
            raise ValueError("Expected population in the region, but the value is too small!")

        return value
    except ValueError:
        raise ValidationError(f"Expected population in the region, but got {value}:{type(value)}!")
