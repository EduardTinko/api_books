import json
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.views import View

# Create your views here.
from .models import Author, Book


class AuthorsView(View):
    @staticmethod
    def json_authors(list_authors):
        return JsonResponse(
            {
                "authors": [
                    {
                        "id": author.id,
                        "name": author.name,
                        "books": [
                            {
                                "id": book.id,
                                "name": book.name,
                                "genre": book.genre,
                                "publication_date": book.publication_date,
                            }
                            for book in Book.objects.filter(author_id=author.id)
                        ],
                    }
                    for author in list_authors
                ]
            }
        )

    def get(self, request, author_id=None):
        if request.method == "GET":
            if author_id:
                try:
                    list_authors = Author.objects.get(pk=author_id)
                    return self.json_authors([list_authors])
                except Author.DoesNotExist:
                    return JsonResponse(
                        {"error": f"Автора з ID: {author_id} не знайдено."}, status=404
                    )
            else:
                name_filter = request.GET.get("name", None)
                if name_filter:
                    list_authors = Author.objects.filter(name__icontains=name_filter)
                    if not list_authors.exists():
                        return JsonResponse(
                            {"error": f"Авторів {name_filter} не знайдено."}, status=404
                        )
                    return self.json_authors(list_authors)
                else:
                    list_authors = Author.objects.all()
                return self.json_authors(list_authors)

    @staticmethod
    def post(request):
        try:
            author_json = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": f"Невірний формат Json!"}, status=400)
        try:
            Author(**author_json).full_clean()
            Author.objects.create(**author_json)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"message": "Автора додано"}, status=200)


class BooksView(View):
    @staticmethod
    def json_books(list_books):
        return JsonResponse(
            {
                "books": [
                    {
                        "id": book.id,
                        "name": book.name,
                        "author": {"id": book.author.id, "name": book.author.name},
                        "genre": book.genre,
                        "publication_date": book.publication_date,
                    }
                    for book in list_books
                ]
            }
        )

    def get(self, request, book_id=None):
        if book_id:
            try:
                list_books = Book.objects.get(pk=book_id)
                return self.json_books([list_books])
            except Book.DoesNotExist:
                return JsonResponse(
                    {"error": f"Книгу з ID: {book_id} не знайдено."}, status=404
                )

        else:
            filter_books = request.GET.items()
            if not filter_books:
                list_books = Book.objects.all()
                return self.json_books(list_books)

            filter_name = request.GET.get("name")
            filter_author = request.GET.get("author")
            filter_genre = request.GET.get("genre")
            filter_publication_date = request.GET.get("publication_date")

            all_filter_books = Q()
            if filter_name:
                all_filter_books &= Q(name__icontains=filter_name)
            if filter_author:
                all_filter_books &= Q(author__name__icontains=filter_author)
            if filter_genre:
                all_filter_books &= Q(genre__icontains=filter_genre)
            if filter_publication_date:
                try:
                    filter_publication_date = datetime.strptime(
                        filter_publication_date, "%Y-%m-%d"
                    ).date()
                except ValueError:
                    return JsonResponse(
                        {
                            "error": f"{filter_publication_date} value has an invalid date format. "
                            f"It must be in YYYY-MM-DD format."
                        },
                        status=400,
                    )
                all_filter_books &= Q(publication_date=filter_publication_date)

            list_books = Book.objects.filter(all_filter_books)
            if not list_books.exists():
                return JsonResponse({"error": f"Книги не знайдено!"}, status=404)
            return self.json_books(list_books)

    @staticmethod
    def post(request):
        try:
            book_json = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": f"Невірний формат Json!"}, status=400)

        try:
            author_json = book_json.get("author")
            if author_json:
                author, created = Author.objects.get_or_create(name=author_json)
                book_json["author"] = author
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=404)
        try:
            Book(**book_json).full_clean()
            Book.objects.create(**book_json)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"message": "Книгу додано"}, status=200)

    @staticmethod
    def put(request, book_id=None):
        if book_id is None:
            return JsonResponse({"error": f"Передайте значення ID"}, status=404)
        try:
            book = Book.objects.get(pk=book_id)
            book_json = json.loads(request.body)
        except Book.DoesNotExist:
            return JsonResponse(
                {"error": f"Книгу з ID: {book_id} не знайдено."}, status=404
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": f"Невірний формат Json!"}, status=400)

        try:
            author_json = book_json.get("author")
            if author_json:
                author, created = Author.objects.get_or_create(name=author_json)
                book_json["author"] = author

            for key, value in book_json.items():
                if key != "author":
                    setattr(book, key, value)

            book.full_clean()
            book.save()

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({"message": "Книгу оновлено"}, status=200)

    @staticmethod
    def delete(request, book_id=None):
        if book_id is None:
            return JsonResponse({"error": f"Передайте значення ID"}, status=404)
        try:
            book = Book.objects.get(pk=book_id)
            book.delete()
        except Book.DoesNotExist:
            return JsonResponse(
                {"error": f"Книгу з ID: {book_id} не знайдено."}, status=404
            )
        return JsonResponse({"message": "Книга успішно видалена"}, status=200)
