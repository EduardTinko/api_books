import json

import pytest
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from books.models import Author
from books.views import AuthorList, AuthorDetail


@pytest.mark.django_db
class TestAuthor(TestCase):
    def setUp(self):
        call_command("flush", "--noinput")
        call_command("loaddata", "test_books.json")

    def test_get_author_list(self):
        factory = APIRequestFactory()
        request = factory.get("/")
        response = AuthorList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == [
            {"id": 1, "name": "Leonardo"},
            {"id": 2, "name": "Jhon Smit"},
        ]

    def test_get_author_empty(self):
        Author.objects.all().delete()

        factory = APIRequestFactory()
        request = factory.get("/authors")
        response = AuthorList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == []

    def test_get_author_filter_name(self):
        factory = APIRequestFactory()
        request = factory.get("/", {"name": "Leona"})
        response = AuthorList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == [{"id": 1, "name": "Leonardo"}]

    def test_get_author_incorrect_filter_name(self):
        factory = APIRequestFactory()
        request = factory.get("/", {"name": "Ivan"})
        response = AuthorList.as_view()(request)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == []

    def test_get_author_id(self):
        factory = APIRequestFactory()
        request = factory.get("/")
        response = AuthorDetail.as_view()(request, pk=1)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == {"id": 1, "name": "Leonardo"}

    def test_get_author_incorrect_id(self):
        factory = APIRequestFactory()
        request = factory.get("/")
        response = AuthorDetail.as_view()(request, pk=3)
        response.render()
        assert response.status_code == 404
        assert json.loads(response.content) == {"detail": "Not found."}

    def test_post_author_add(self):
        factory = APIRequestFactory()
        request = factory.post("/", {"name": "New Leonardo"})
        response = AuthorList.as_view()(request)
        response.render()
        assert response.status_code == 201
        assert json.loads(response.content) == {"id": 3, "name": "New Leonardo"}

    def test_post_author_incorrect_add(self):
        factory = APIRequestFactory()
        request = factory.post("/", {"name": ""})
        response = AuthorList.as_view()(request)
        response.render()
        assert response.status_code == 400
        assert json.loads(response.content) == {
            "name": ["This field may not be blank."]
        }

    def test_post_author_add_short_value(self):
        factory = APIRequestFactory()
        request = factory.post("/", {"name": "S"})
        response = AuthorList.as_view()(request)
        response.render()
        assert response.status_code == 400
        assert json.loads(response.content) == {"name": ["Value is too short."]}
