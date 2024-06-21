from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_zero_or_more(value):
    if value < 0:
        raise ValidationError(
            _("%(value)s is less than zero"),
            params={"value": value},
        )
