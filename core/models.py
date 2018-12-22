from djongo import models
from django import forms

import datetime
from django.core.exceptions import ValidationError


def validate_year_min_max(value):
    now = datetime.datetime.now()
    if value < 1000 or value > now.year:
        raise ValidationError('Fecha errada. Libro muy antiguo o aún no publicado.', code='badyear')


def min_value(value):
    if value < 0:
        raise ValidationError('Número negativo', code='badnumber')


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BookContent(models.Model):
    #author = models.CharField(max_length=100, null=False, blank=False)
    year = models.IntegerField(null=False,blank=False, validators=(validate_year_min_max,))
    edition = models.IntegerField(null=False, blank=False, validators=(min_value,))
    image = models.TextField(null=False, blank=True)
    copies = models.IntegerField(null=False, validators=(min_value,))
    rating = models.IntegerField(null=False, blank=True)

    class Meta:
        abstract = True


# para acceder desde DJANGO ADMIN
"""class BookForm(models.Model):

    class Meta:
        model = BookContent
        fields = (
            'title', 'author', 'year', 'edition', 'image', 'copies'
        )
"""


class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.EmbeddedModelField(
        model_container=BookContent,
    )
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title
