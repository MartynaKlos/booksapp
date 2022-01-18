from cmath import pi
import requests

from urllib.request import Request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, UpdateView

from rest_framework import viewsets

from booksapp.local_settings import API_KEY
from .forms import AddBookForm, FindBookForm
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AllBooksView(ListView):
    queryset = Book.objects.all()
    context_object_name = 'books'
    template_name = 'allbooks.html'


class AddBookView(FormView):
    form_class = AddBookForm
    template_name = 'add-book.html'
    success_url = reverse_lazy('all-books')


class UpdateBookView(UpdateView):
    model = Book
    form_class = AddBookForm
    template_name = 'update-book.html'
    success_url = reverse_lazy('all-books')
    pk_url_kwarg = 'book_pk'


# class AddBookFromGoogle(View):
#     def get(self, request, *args, **kwargs):
#         form = FindBookForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'add-book.html', context)

#     def post(self, request, *args, **kwargs):
#         form = FindBookForm(request.POST)
#         context = {
#             'form': form
#         }
#         if form.is_valid():
#             author = form.cleaned_data['author']
#             url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}&key={API_KEY}'
#             response = requests.get(url).json()
#             bookinfo = response['items'][1]['volumeInfo']
#             author = bookinfo['authors'][0]
#             pub_date = bookinfo['publishedDate']
#             title = bookinfo['title']
#             pages = bookinfo['pageCount']
#             language = bookinfo['language']
#             isbn = bookinfo['industryIdentifiers'][0]['identifier']
#             Book.objects.create(title=title, author=author, publication_date=pub_date, pages=pages, language=language)
#             context['api_response'] = bookinfo
#             return render(request, 'api.html', context)


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
        bookinfo = response['items'][0]['volumeInfo']
        author = bookinfo['authors'][0]
        pub_date = bookinfo['publishedDate']
        title = bookinfo['title']
        pages = bookinfo['pageCount']
        language = bookinfo['language']
        isbn = bookinfo['industryIdentifiers'][0]['identifier']
        Book.objects.create(title=title, author=author, publication_date=pub_date, pages=pages, language=language, isbn=isbn)
        return super().form_valid(form)
