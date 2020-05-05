from django import forms
from .models import City, Book
from django.forms import ModelForm, TextInput

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={
            'class': 'form-control',
             'name': 'city',
              'id': 'city',
                'placeholder': 'Введите город'
                   })}

class BooksForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf', 'cover')