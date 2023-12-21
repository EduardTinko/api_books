import json

import pytest
from rest_framework.test import APIRequestFactory

from books.models import Author
from books.views import AuthorList, AuthorDetail


@pytest.mark.django_db
def test_get_author_list():
    factory = APIRequestFactory()
    request = factory.get("/")
    response = AuthorList.as_view()(request)
    response.render()
    assert response.status_code == 200
    assert json.loads(response.content) == [
        {"id": 1, "name": "Leonardo"},
        {"id": 2, "name": "Jhon Smit"},
    ]


@pytest.mark.django_db
def test_get_author_empty():
    Author.objects.all().delete()

    factory = APIRequestFactory()
    request = factory.get("/authors")
    response = AuthorList.as_view()(request)
    response.render()
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.django_db
def test_get_author_filter_name():
    factory = APIRequestFactory()
    request = factory.get("/", {"name": "Leona"})
    response = AuthorList.as_view()(request)
    response.render()
    assert response.status_code == 200
    assert json.loads(response.content) == [{"id": 1, "name": "Leonardo"}]


@pytest.mark.django_db
def test_get_author_incorrect_filter_name():
    factory = APIRequestFactory()
    request = factory.get("/", {"name": "Ivan"})
    response = AuthorList.as_view()(request)
    response.render()
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.django_db
def test_get_author_id():
    factory = APIRequestFactory()
    request = factory.get("/")
    response = AuthorDetail.as_view()(request, pk=1)
    response.render()
    assert response.status_code == 200
    assert json.loads(response.content) == {"id": 1, "name": "Leonardo"}


@pytest.mark.django_db
def test_get_author_incorrect_id():
    factory = APIRequestFactory()
    request = factory.get("/")
    response = AuthorDetail.as_view()(request, pk=3)
    response.render()
    assert response.status_code == 404
    assert json.loads(response.content) == {"detail": "Not found."}


@pytest.mark.django_db
def test_post_author_add():
    factory = APIRequestFactory()
    request = factory.post("/", {"name": "New Leonardo"})
    response = AuthorList.as_view()(request)
    response.render()
    assert response.status_code == 201
    assert json.loads(response.content) == {"id": 3, "name": "New Leonardo"}


@pytest.mark.django_db
def test_post_author_incorrect_add():
    factory = APIRequestFactory()
    request = factory.post("/", {"name": ""})
    response = AuthorList.as_view()(request)
    response.render()
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field may not be blank."]}


@pytest.mark.django_db
def test_post_author_add_short_value():
    factory = APIRequestFactory()
    request = factory.post("/", {"name": "S"})
    response = AuthorList.as_view()(request)
    response.render()
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["Value is too short."]}
