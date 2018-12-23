from django import forms
from .models import validate_year_min_max, min_value
from django.views.generic import UpdateView
from .models import Author

class BookForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label='Título')
    year = forms.IntegerField(required=False, label='Año')
    author = forms.CharField(max_length=100,required=False, label='Autor')


class AuthorFormAdd(forms.Form):
    name = forms.CharField(max_length=100)


class BookFormAdd(forms.Form):
    title = forms.CharField(max_length=100, label='Título',required=False)
    year = forms.IntegerField(validators=(validate_year_min_max,), label='Año',required=False)
    edition = forms.IntegerField(validators=(min_value,), label='Edición', required=False)
    image = forms.FileField(label='Imagen', required=False)
    copies = forms.IntegerField(validators=(min_value,), label='Ejemplares', required=False)
    rating = forms.IntegerField(label='Rating',required=False)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), label='Autores', required=False)

