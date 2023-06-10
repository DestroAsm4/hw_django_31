from rest_framework.exceptions import ValidationError

def check_not_published(value):

    if value:
        raise ValidationError("Значение не может быть True")