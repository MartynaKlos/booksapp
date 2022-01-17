from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, UpdateView

from rest_framework import viewsets

from .forms import AddBookForm
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