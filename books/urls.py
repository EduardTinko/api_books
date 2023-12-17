from django.urls import path

from books.views import authors

urlpatterns = [
    path("authors/", authors, name="authors"),
]
