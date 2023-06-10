from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import TextChoices

from app.settings import FORBIDDEN_DOMAIN
from users.validators import check_age


class UserRoles(TextChoices):
    MEMBER = 'member', 'Пользователь'
    ADMIN = 'admin', 'Админ'
    MODERATOR = 'moderator', 'Модератор'


class User(AbstractUser):


    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    locations = models.ManyToManyField('Location')
    birth_date = models.DateField(null=True, blank=True, validators=[check_age])
    email = models.EmailField(validators=[RegexValidator(
        regex=FORBIDDEN_DOMAIN,
        message='Нельзя с такого домена',
        inverse_match=True
    )],
        unique=True
    )

    def save(self, *args, **kwargs):
        self.set_password(raw_password=self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'





class Location(models.Model):

    name = models.CharField(max_length=100, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,

        }

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
