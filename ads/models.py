from django.db import models
import csv

from users.models import User


class Ad(models.Model):

    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey('ads.Categories', on_delete=models.CASCADE)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='ad_image', blank=True, null=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author.first_name,
            'price': self.price,
            'description': self.description,
            'is_published': self.is_published,
            'category': self.category.name,
            'image': self.image.url if self.image else None

        }

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name


class Categories(models.Model):

    name = models.CharField(max_length=30)

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


