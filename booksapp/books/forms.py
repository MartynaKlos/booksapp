from django.forms import forms, ModelForm

from .models import Book


class AddBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 
                'author', 
                'isbn', 
                'publication_date', 
                'pages', 
                'language']
