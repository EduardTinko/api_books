import json

import pytest
from django.test import RequestFactory

from books.views import AuthorsView


@pytest.mark.django_db
def test_get_author_list():
    request = RequestFactory().get("/")
    authors_view = AuthorsView()
    response = authors_view.get(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "authors": [
            {
                "id": 1,
                "name": "Leonardo",
                "books": [
                    {
                        "genre": "horror",
                        "id": 1,
                        "name": "Red Book",
                        "publication_date": "2012-12-12",
                    }
                ],
            },
            {
                "id": 2,
                "name": "Jhon Smit",
                "books": [
                    {
                        "genre": "Comedy",
                        "id": 2,
                        "name": "Derby",
                        "publication_date": "2020-12-12",
                    }
                ],
            },
        ]
    }


@pytest.mark.django_db
def test_get_author_id():
    request = RequestFactory().get("/")
    authors_view = AuthorsView()
    response = authors_view.get(request, 2)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "authors": [
            {
                "id": 2,
                "name": "Jhon Smit",
                "books": [
                    {
                        "genre": "Comedy",
                        "id": 2,
                        "name": "Derby",
                        "publication_date": "2020-12-12",
                    }
                ],
            },
        ]
    }


@pytest.mark.django_db
def test_get_author_no_id():
    request = RequestFactory().get("/")
    authors_view = AuthorsView()
    response = authors_view.get(request, 3)
    assert response.status_code == 404
    assert json.loads(response.content) == {"error": "Автора з ID: 3 не знайдено."}


@pytest.mark.django_db
def test_get_author_id():
    request = RequestFactory().get(
        "/",
        {
            "name": "Leonardo",
        },
        content_type="application/json",
    )
    authors_view = AuthorsView()
    response = authors_view.get(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "authors": [
            {
                "id": 1,
                "name": "Leonardo",
                "books": [
                    {
                        "genre": "horror",
                        "id": 1,
                        "name": "Red Book",
                        "publication_date": "2012-12-12",
                    }
                ],
            }
        ]
    }


@pytest.mark.django_db
def test_post_author_add():
    request = RequestFactory().post(
        "/",
        {
            "name": "New Leonardo",
        },
        content_type="application/json",
    )
    authors_view = AuthorsView()
    response = authors_view.post(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {"message": "Автора додано"}


@pytest.mark.django_db
def test_post_author_empty_request():
    request = RequestFactory().post(
        "/",
        {},
    )
    authors_view = AuthorsView()
    response = authors_view.post(request)
    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Невірний формат Json!"}
