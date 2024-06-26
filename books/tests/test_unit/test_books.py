import json

import pytest
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from books.models import Book
from books.views import BookList, BookDetail


@pytest.mark.django_db
class TestAuthor(TestCase):
    def setUp(self):
        call_command("flush", "--noinput")
        call_command("loaddata", "test_books.json")

    def test_get_book_list(self):
        factory = APIRequestFactory()
        request = factory.get("/")
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == [
            {
                "id": 1,
                "author": {"id": 1, "name": "Leonardo"},
                "genre": "horror",
                "name": "Red Book",
                "publication_date": "2012-12-12",
            },
            {
                "id": 2,
                "author": {"id": 2, "name": "Jhon Smit"},
                "genre": "Comedy",
                "name": "Derby",
                "publication_date": "2020-12-12",
            },
        ]

    def test_get_book_empty(self):
        Book.objects.all().delete()

        factory = APIRequestFactory()
        request = factory.get("/")
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == []

    def test_get_book_id(self):
        factory = APIRequestFactory()
        request = factory.get("/")
        response = BookDetail.as_view()(request, pk=1)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == {
            "id": 1,
            "author": {"id": 1, "name": "Leonardo"},
            "genre": "horror",
            "name": "Red Book",
            "publication_date": "2012-12-12",
        }

    def test_get_book_incorrect_id(self):
        factory = APIRequestFactory()
        request = factory.get("/")
        response = BookDetail.as_view()(request, pk=4)
        response.render()
        assert response.status_code == 404
        assert json.loads(response.content) == {"detail": "Not found."}

    def test_get_book_filter_all(self):
        factory = APIRequestFactory()
        request = factory.get(
            "/",
            {
                "author__name": "Leo",
                "genre": "horror",
                "name": "Red",
                "publication_date": "2012-12-12",
                "publication_date__year": "2012",
                "publication_date__day": "12",
                "publication_date__month": "12",
            },
        )
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == [
            {
                "id": 1,
                "author": {"id": 1, "name": "Leonardo"},
                "genre": "horror",
                "name": "Red Book",
                "publication_date": "2012-12-12",
            }
        ]

    def test_get_book_filter_no_month(self):
        factory = APIRequestFactory()
        request = factory.get(
            "/",
            {
                "author__name": "Leo",
                "genre": "horror",
                "name": "Red",
                "publication_date": "2012-12-12",
                "publication_date__year": "2012",
                "publication_date__day": "12",
                "publication_date__month": "1",
            },
        )
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == []

    def test_get_book_filter_no_name_genre(self):
        factory = APIRequestFactory()
        request = factory.get(
            "/",
            {
                "author__name": "Leo",
                "genre": "no",
                "name": "no",
                "publication_date": "2012-12-12",
                "publication_date__year": "2012",
                "publication_date__day": "12",
                "publication_date__month": "12",
            },
        )
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == []

    def test_get_book_filter_incorrect_date(self):
        factory = APIRequestFactory()
        request = factory.get(
            "/",
            {
                "author__name": "Leo",
                "genre": "horror",
                "name": "Red",
                "publication_date": "2012-122-12",
                "publication_date__year": "2012",
                "publication_date__day": "12",
                "publication_date__month": "12",
            },
        )
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 400
        assert json.loads(response.content) == {
            "publication_date": ["Enter a valid date."]
        }

    def test_post_book_add(self):
        factory = APIRequestFactory()
        request = factory.post(
            "/",
            {
                "author": {"name": "2 Leo"},
                "genre": "New_horror2",
                "name": "NewBook2",
                "publication_date": "2020-10-10",
            },
            format="json",
        )
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 201
        assert json.loads(response.content) == {
            "id": 3,
            "author": {"id": 3, "name": "2 Leo"},
            "genre": "New_horror2",
            "name": "NewBook2",
            "publication_date": "2020-10-10",
        }

    def test_post_book_add_incorrect_author(self):
        factory = APIRequestFactory()
        request = factory.post(
            "/",
            {
                "author": {"name": "N"},
                "genre": "New_horror",
                "name": "NewBook",
                "publication_date": "2020-10-20",
            },
            format="json",
        )
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 400
        assert json.loads(response.content) == {
            "author": {"name": ["Value is too short."]}
        }

    def test_post_book_add_incorrect_name_genre(self):
        factory = APIRequestFactory()
        request = factory.post(
            "/",
            {
                "author": {"name": "Name"},
                "genre": "N",
                "name": "N",
                "publication_date": "2020-10-20",
            },
            format="json",
        )
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 400
        assert json.loads(response.content) == {
            "genre": ["Value is too short."],
            "name": ["Value is too short."],
        }

    def test_post_book_add_incorrect_date(self):
        factory = APIRequestFactory()
        request = factory.post(
            "/",
            {
                "author": {"name": "Name"},
                "genre": "New",
                "name": "New",
                "publication_date": "2020-102-20",
            },
            format="json",
        )
        response = BookList.as_view()(request)
        response.render()
        assert response.status_code == 400
        assert json.loads(response.content) == {
            "publication_date": [
                "Date has wrong format. Use one of these formats "
                "instead: YYYY-MM-DD."
            ]
        }

    def test_put_book_incorrect_request(self):
        factory = APIRequestFactory()
        request = factory.put(
            "/",
            {
                "author": {"name": "N"},
                "genre": "N",
                "name": "N",
                "publication_date": "2020-102-20",
            },
            format="json",
        )
        response = BookDetail.as_view()(request, pk=1)
        response.render()
        assert response.status_code == 400
        assert json.loads(response.content) == {
            "author": {"name": ["Value is too short."]},
            "genre": ["Value is too short."],
            "name": ["Value is too short."],
            "publication_date": [
                "Date has wrong format. Use one of these formats "
                "instead: YYYY-MM-DD."
            ],
        }

    def test_put_book_correct_request(self):
        factory = APIRequestFactory()
        request = factory.put(
            "/",
            {
                "author": {"name": "New"},
                "genre": "Name",
                "name": "New",
                "publication_date": "2020-10-20",
            },
            format="json",
        )
        response = BookDetail.as_view()(request, pk=1)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == {
            "id": 1,
            "author": {"id": 3, "name": "New"},
            "genre": "Name",
            "name": "New",
            "publication_date": "2020-10-20",
        }

    def test_put_book_incorrect_id(self):
        factory = APIRequestFactory()
        request = factory.put(
            "/",
            {
                "author": {"name": "New"},
                "genre": "Name",
                "name": "New",
                "publication_date": "2020-10-20",
            },
            format="json",
        )
        response = BookDetail.as_view()(request, pk=3)
        response.render()
        assert response.status_code == 404
        assert json.loads(response.content) == {"detail": "Not found."}

    def test_delete_book(self):
        factory = APIRequestFactory()
        request = factory.delete("/")
        response = BookDetail.as_view()(request, pk=1)
        response.render()
        assert response.status_code == 204
        book = Book.objects.filter(pk=1)
        assert not book.exists()
