import pytest

from books.models import Book
from booksapp.booksapp.books.tests.utils import set_random_date


@pytest.mark.django_db
def test_books_list_view(set_up, client):
    url = '/all-books/'
    response = client.get(url)
    list_view = list(response.context['books'])
    list_db = list(Book.objects.all())
    assert response.status_code == 200
    assert list_db == list_view


@pytest.mark.django_db
def test_add_book_view(set_up, client):
    url = '/add-book/'
    data = {
            'title': 'Nowa książka',
            'author': 'Jan Kowalski',
            'publication_date': set_random_date(),
            'pages': 120,
            'isbn': '1234567891234',
            'language': 'pl',
            'cover_url': 'https://cover_url.com'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Book.objects.all().count() == 6


@pytest.mark.django_db
def test_update_book_view(set_up, client):
    book = Book.objects.all().order_by('?').first()
    url = f'/update-book/{book.pk}/'
    data = {
        'title': book.title,
        'author': book.author,
        'publication_date': book.publication_date,
        'pages': 555,
        'isbn': book.isbn,
        'language': 'fr',
        'cover_url': book.cover_url
    }
    response = client.post(url, data)
    assert response.status_code == 302
    book.refresh_from_db()
    assert book.pages == 555
    assert book.language == 'fr'