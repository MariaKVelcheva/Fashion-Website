from django.core.exceptions import ValidationError


def name_validator(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError("Your name must only contain letters.")
