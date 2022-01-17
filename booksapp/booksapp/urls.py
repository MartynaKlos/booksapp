"""booksapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

import books.views as books


router = DefaultRouter()
router.register(r'books', books.BookViewSet, basename='books')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all-books/', books.AllBooksView.as_view(), name='all-books'),
    path('add-book/', books.AddBookView.as_view(), name='add-book'),
    path('update-book/<int:book_pk>/', books.UpdateBookView.as_view(), name='update-book'),
    path('api/', include((router.urls, 'books'), namespace='api-books')),
]
