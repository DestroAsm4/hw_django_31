from django.core.validators import MinLengthValidator
from django.db import models
import csv

from users.models import User


class Ad(models.Model):

    name = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('ads.Categories', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='ad_image', blank=True, null=True)



    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name

class Selection(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    def __str__(self):
        return self.name


class Categories(models.Model):

    name = models.CharField(max_length=30)
    slug = models.SlugField(
        max_length=10,
        validators=[MinLengthValidator(5)],
        unique=True
    )


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


