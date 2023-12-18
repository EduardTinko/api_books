import json

import pytest
from django.test import RequestFactory

from books.models import Book
from books.views import BooksView


@pytest.mark.django_db
def test_get_book_list():
    request = RequestFactory().get("/")
    books_view = BooksView()
    response = books_view.get(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "books": [
            {
                "id": 1,
                "name": "Red Book",
                "author": {"id": 1, "name": "Leonardo"},
                "genre": "horror",
                "publication_date": "2012-12-12",
            },
            {
                "id": 2,
                "name": "Derby",
                "author": {"id": 2, "name": "Jhon Smit"},
                "genre": "Comedy",
                "publication_date": "2020-12-12",
            },
        ]
    }


@pytest.mark.django_db
def test_get_book_empty():
    Book.objects.all().delete()

    request = RequestFactory().get("/")
    books_view = BooksView()
    response = books_view.get(request)
    assert response.status_code == 404
    assert json.loads(response.content) == {"error": "Книги не знайдено!"}


@pytest.mark.django_db
def test_get_book_id():
    request = RequestFactory().get("/")
    books_view = BooksView()
    response = books_view.get(request, 1)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "books": [
            {
                "id": 1,
                "name": "Red Book",
                "author": {"id": 1, "name": "Leonardo"},
                "genre": "horror",
                "publication_date": "2012-12-12",
            }
        ]
    }


@pytest.mark.django_db
def test_get_book_no_id():
    request = RequestFactory().get("/")
    books_view = BooksView()
    response = books_view.get(request, 4)
    assert response.status_code == 404
    assert json.loads(response.content) == {"error": "Книгу з ID: 4 не знайдено."}


@pytest.mark.django_db
def test_get_book_filter_all():
    request = RequestFactory().get(
        "/",
        {
            "name": "Red Book",
            "author": "Leonardo",
            "genre": "horror",
            "publication_date": "2012-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.get(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "books": [
            {
                "id": 1,
                "name": "Red Book",
                "author": {"id": 1, "name": "Leonardo"},
                "genre": "horror",
                "publication_date": "2012-12-12",
            }
        ]
    }


@pytest.mark.django_db
def test_get_book_filter_name_date():
    request = RequestFactory().get(
        "/",
        {
            "name": "Der",
            "publication_date": "2020-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.get(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "books": [
            {
                "id": 2,
                "name": "Derby",
                "author": {"id": 2, "name": "Jhon Smit"},
                "genre": "Comedy",
                "publication_date": "2020-12-12",
            },
        ]
    }


@pytest.mark.django_db
def test_get_book_filter_empty():
    request = RequestFactory().get(
        "/",
        {
            "name": "Derby",
            "publication_date": "2000-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.get(request)
    assert response.status_code == 404
    assert json.loads(response.content) == {"error": "Книги не знайдено!"}


@pytest.mark.django_db
def test_get_book_filter_no_correct():
    request = RequestFactory().get(
        "/",
        {
            "name1": "Derby",
            "publication_date": "20001-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.get(request)
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": "20001-12-12 value has an invalid date format. It must be in YYYY-MM-DD format."
    }


@pytest.mark.django_db
def test_post_book_empty_request():
    request = RequestFactory().post("/")
    books_view = BooksView()
    response = books_view.post(request)
    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Невірний формат Json!"}


@pytest.mark.django_db
def test_post_book():
    request = RequestFactory().post(
        "/",
        {
            "name": "New book",
            "author": {"name": "new Jhon"},
            "genre": "new horror",
            "publication_date": "2020-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.post(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {"message": "Книгу додано"}


@pytest.mark.django_db
def test_post_book_validator_error_date():
    request = RequestFactory().post(
        "/",
        {
            "name": "New book",
            "author": {"name": "new Jhon"},
            "genre": "new horror",
            "publication_date": "new2020-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.post(request)
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": "{'publication_date': ['“new2020-12-12” value has an invalid date "
        "format. It must be in YYYY-MM-DD format.']}"
    }


@pytest.mark.django_db
def test_post_book_validator_error():
    request = RequestFactory().post(
        "/",
        {
            "name": "N",
            "author": {"name": "s"},
            "genre": "",
            "publication_date": "2020-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.post(request)
    assert response.status_code == 400
    assert (
        json.loads(response.content)
        == {
            "error": "{'name': ['Занадто коротке значення'], 'genre': ['This field cannot "
            "be blank.']}"
        }
        != {
            "error": "{'publication_date': ['“new2020-12-12” value has an invalid date "
            "format. It must be in YYYY-MM-DD format.']}"
        }
    )


@pytest.mark.django_db
def test_put_book_bead_request():
    request = RequestFactory().put("/")
    books_view = BooksView()
    response = books_view.post(request)
    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Невірний формат Json!"}


@pytest.mark.django_db
def test_put_book_id():
    request = RequestFactory().put(
        "/",
        {
            "name": "edit book",
            "author": {"name": "edit Jhon"},
            "genre": "edit horror",
            "publication_date": "2020-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.put(request, 4)
    assert response.status_code == 404
    assert json.loads(response.content) == {"error": "Книгу з ID: 4 не знайдено."}


@pytest.mark.django_db
def test_put_book_id_no_edit():
    request = RequestFactory().put("/")
    books_view = BooksView()
    response = books_view.put(request, 2)
    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Невірний формат Json!"}


@pytest.mark.django_db
def test_put_book_id_edit():
    request = RequestFactory().put(
        "/",
        {
            "name": "edit book",
            "author": {"name": "edit Jhon"},
            "genre": "edit horror",
            "publication_date": "2020-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.put(request, 2)
    assert response.status_code == 200
    assert json.loads(response.content) == {"message": "Книгу оновлено"}


@pytest.mark.django_db
def test_put_book_edit_bead_format():
    request = RequestFactory().put(
        "/",
        {
            "name": "edit book",
            "author": {"name": "edit Jhon"},
            "genre": "edit horror",
            "publication_date": "new2020-12-12",
        },
        content_type="application/json",
    )
    books_view = BooksView()
    response = books_view.put(request, 2)
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": "{'publication_date': ['“new2020-12-12” value has an invalid date "
        "format. It must be in YYYY-MM-DD format.']}"
    }


@pytest.mark.django_db
def test_delete_book_id():
    request = RequestFactory().delete("/")
    books_view = BooksView()
    response = books_view.delete(request, 2)
    assert response.status_code == 200
    assert json.loads(response.content) == {"message": "Книга успішно видалена"}


@pytest.mark.django_db
def test_delete_book_no_id():
    request = RequestFactory().delete("/")
    books_view = BooksView()
    response = books_view.delete(request, 3)
    assert response.status_code == 404
    assert json.loads(response.content) == {"error": "Книгу з ID: 3 не знайдено."}
