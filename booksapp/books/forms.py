from sqlite3 import Date
from django.forms import forms, ModelForm, widgets, DateInput, DateField

from .models import Book


class AddBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 
                  'author', 
                  'isbn', 
                  'publication_date', 
                  'pages', 
                  'language',
                  'cover_url']
        widgets = {
            'publication_date': DateInput(attrs={'type': 'date'})
        }


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


class SearchBookForm(ModelForm):
    start_date = DateField(widget=widgets.DateInput(attrs={'type': 'date'}))
    end_date = DateField(widget=widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Book
        fields = ['title', 
                'author', 
                'language']

    def __init__(self, *args, **kwargs):
        super(FindBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['author'].required = False
        self.fields['language'].required = False
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False