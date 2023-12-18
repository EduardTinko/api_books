from django.urls import path

from books.views import AuthorsView, BooksView

urlpatterns = [
    path("authors/", AuthorsView.as_view(), name="authors"),
    path("authors/<int:author_id>/", AuthorsView.as_view(), name="authors"),
    path("books/", BooksView.as_view(), name="books"),
    path("books/<int:book_id>/", BooksView.as_view(), name="books"),
]
