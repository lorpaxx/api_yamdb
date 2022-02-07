from datetime import date
from django.core.exceptions import ValidationError


def validate_year(value):
    now_year = date.today().year
    if value > now_year:
        raise ValidationError(
            f'{value} ещё не наступил!'
        )
    # return value
