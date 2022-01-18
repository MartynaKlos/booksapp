from django.forms import forms, Form, ModelForm

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


class FindBookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['title', 
                  'author', 
                  'isbn']

    def __init__(self, *args, **kwargs):
        super(FindBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['author'].required = False
        self.fields['isbn'].required = False
        