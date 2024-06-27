import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


def validate_zero_or_more(value):
    """validate number if number >= 0"""
    if value < 0:
        raise ValidationError(
            _("%(value)s is less than zero"),
            params={"value": value},
        )


def validate_username(value):
    """validate username"""
    if len(value) < 8 or len(value) > 150:
        raise serializers.ValidationError(
            _("username must be between 3 and 150 characters long")
        )

    if not re.match(r'^\w+$', value):
        raise serializers.ValidationError(
            _("username must contain only letters, numbers, and underscores")
        )

    if value.isdigit():
        raise serializers.ValidationError(
            _("username cannot consist only of digits")
        )

    letter_count = sum(1 for char in value if char.isalpha())
    if letter_count < 3:
        raise serializers.ValidationError(
            _("username must contain at least 3 letters")
        )

    return value
