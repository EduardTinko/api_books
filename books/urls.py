from django.urls import path
from books.views import AuthorList, AuthorDetail, BookList, BookDetail

urlpatterns = [
    path("authors/", AuthorList.as_view(), name="authors"),
    path("authors/<int:pk>", AuthorDetail.as_view(), name="authors"),
    path("books/", BookList.as_view(), name="books"),
    path("books/<int:pk>", BookDetail.as_view(), name="books"),
]
