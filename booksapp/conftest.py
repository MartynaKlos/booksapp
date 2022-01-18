import random

from faker import Faker
import pytest
from random import randint

from books.models import Book
from books.tests.utils import set_random_date

faker = Faker("pl_PL")


@pytest.fixture
def set_up():
    for i in range(5):
        Book.objects.create(
            title=faker.word(),
            author=faker.name(),
            publication_date=set_random_date(),
            pages=randint(100, 400),
            isbn=faker.isbn13(),
            language=faker.word(),
            cover_url=faker.domain_name()
        )
 