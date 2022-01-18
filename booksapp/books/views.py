from cmath import pi
from re import template
import requests

from urllib.request import Request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, TemplateView

from rest_framework import viewsets, filters

from booksapp.local_settings import API_KEY
from .forms import AddBookForm, FindBookForm, SearchBookForm
from .models import Book
from .serializers import BookSerializer


class MainView(TemplateView):
    template_name = 'main.html'


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['author', 'title', 'publication_date']


class AllBooksView(ListView):
    queryset = Book.objects.all()
    context_object_name = 'books'
    template_name = 'allbooks.html'


class SearchBooksView(FormView):
    template_name = 'search_book.html'
    form_class = SearchBookForm
    success_url = reverse_lazy('search-book')

    def form_valid(self, form):
        cd = form.cleaned_data
        context = {
            'form': form
        }

        books = Book.objects.all()
        if cd['title']:
            books = books.filter(title__icontains=cd['title'])
        if cd['author']:
            books = books.filter(author__icontains=cd['author'])
        if cd['start_date']:
            books = books.filter(publication_date__gte=cd['start_date'])
        if cd['end_date']:
            books = books.filter(publication_date__lte=cd['end_date'])

        
        context['books'] = books

        if books.count() == 0:
            context['message'] = "No events matched your search..."
        return render(self.request, 'search_book.html', context)


class AddBookView(FormView):
    form_class = AddBookForm
    template_name = 'add-book.html'
    success_url = reverse_lazy('all-books')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdateBookView(UpdateView):
    model = Book
    form_class = AddBookForm
    template_name = 'update-book.html'
    success_url = reverse_lazy('all-books')
    pk_url_kwarg = 'book_pk'


class AddBookFromGoogle(FormView):
    form_class = FindBookForm
    template_name = 'add-book.html'
    success_url = reverse_lazy('all-books')

    def form_valid(self, form):
        cd = form.cleaned_data

        if not cd['author'] and not cd['title'] and not cd['isbn']:
            return render(self.request, 'add-book.html', {'form': form, 'message': 'Form is empty!'})

        author = cd['author']
        title = cd['title']
        isbn = cd['isbn']

        q_param = 'q='
        if cd['author']:
            q_param += f'+inauthor:{author}'
        if cd['title']:
            q_param += f'+intitle:{title}'
        if cd['isbn']:
            q_param += f'+isbn:{isbn}'

        url = f'https://www.googleapis.com/books/v1/volumes?{q_param}&key={API_KEY}'
        response = requests.get(url).json()
        bookinfo = response['items'][1]['volumeInfo']
        author = bookinfo['authors'][0]
        pub_date = bookinfo['publishedDate']
        title = bookinfo['title']
        pages = int(bookinfo['pageCount'])
        language = bookinfo['language']
        isbn = bookinfo['industryIdentifiers'][0]['identifier']
        cover = bookinfo['imageLinks']['thumbnail']
        Book.objects.create(title=title, author=author, publication_date=pub_date, pages=pages, language=language, isbn=isbn, cover_url=cover)
        return super().form_valid(form)
