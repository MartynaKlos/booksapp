from django.db import models


class Book (models.Model):
    title = models.CharField(max_length=280)
    author = models.CharField(max_length=120)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=20, unique=True)
    pages = models.IntegerField()
    language = models.CharField(max_length=120)
