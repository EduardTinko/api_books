from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics

from .filters import AuthorFilter, BookFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


@method_decorator(cache_page(60 * 5), name="dispatch")
class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_class = AuthorFilter
    search_fields = ["name"]

    @receiver(post_save, sender=Author)
    def authors_clear_cache(sender, instance, **kwargs):
        cache.clear()


@method_decorator(cache_page(60 * 5), name="dispatch")
class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @receiver(post_save, sender=Author)
    def author_clear_cache(sender, instance, **kwargs):
        cache.clear()


@method_decorator(cache_page(60 * 5), name="dispatch")
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    search_fields = ["name"]

    @receiver(post_save, sender=Book)
    def books_clear_cache(sender, instance, **kwargs):
        cache.clear()


@method_decorator(cache_page(60 * 5), name="dispatch")
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @receiver(post_save, sender=Book)
    def book_clear_cache(sender, instance, **kwargs):
        cache.clear()
