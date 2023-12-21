import uuid

import requests
import unittest

API_URL = "http://127.0.0.1:8000/api"


class TestAuthor(unittest.TestCase):
    def setUp(self):
        self.author_name = f"author_name_{str(uuid.uuid4())}"
        self.author_id = None

    def tearDown(self):
        if self.author_id:
            requests.delete(API_URL + f"/authors/{self.author_id}")

    @staticmethod
    def test_get_authors():
        get_authors = requests.get(API_URL + "/authors/")
        get_authors.raise_for_status()
        assert get_authors.status_code == 200

    def test_get_authors_by_id(self):
        self.test_create_author()
        get_author = requests.get(API_URL + f"/authors/{self.author_id}")
        get_author.raise_for_status()
        assert get_author.status_code == 200
        assert get_author.json()["name"] == self.author_name

    def test_create_author(self):
        create = requests.post(API_URL + "/authors/", json={"name": self.author_name})
        create.raise_for_status()
        assert create.status_code == 201
        assert create.json()["name"] == self.author_name
        self.author_id = create.json()["id"]

    def test_filter_author(self):
        self.test_create_author()
        filter_author = requests.get(API_URL + f"/authors/?name={self.author_name}")
        filter_author.raise_for_status()
        assert filter_author.status_code == 200
        assert any(item["name"] == self.author_name for item in filter_author.json())

    def test_delete_author(self):
        self.test_create_author()
        delete = requests.delete(API_URL + f"/authors/{self.author_id}")
        delete.raise_for_status()
        assert delete.status_code == 204
        get_by_id = requests.get(API_URL + f"/authors/{self.author_id}")
        assert get_by_id.status_code == 404
        self.author_id = None

    @staticmethod
    def test_incorrect_create_author():
        create = requests.post(API_URL + "/authors/", json={"name": ""})
        assert create.status_code == 400

    @staticmethod
    def test_get_authors_by_incorrect_id():
        get_author = requests.get(API_URL + f"/authors/sdf")
        assert get_author.status_code == 404


class TestBook(unittest.TestCase):
    def setUp(self):
        self.author_name = f"author_name_{str(uuid.uuid4())}"
        self.author_id = None
        self.book_id = None

    def tearDown(self):
        if self.author_id:
            requests.delete(API_URL + f"/authors/{self.author_id}")
        if self.book_id:
            requests.delete(API_URL + f"/books/{self.book_id}")

    def filter_books(self):
        self.test_create_book()
        book = requests.get(API_URL + f"/books/{self.book_id}")
        return book.json()

    @staticmethod
    def test_get_books():
        get_books = requests.get(API_URL + f"/books/")
        get_books.raise_for_status()
        assert get_books.status_code == 200

    def test_create_book(self):
        post_books = requests.post(
            API_URL + f"/books/",
            json={
                "name": "TestBook",
                "author": {"name": f"{self.author_name}"},
                "genre": "TestGenre",
                "publication_date": "2000-10-10",
            },
        )
        self.book_id = post_books.json()["id"]
        self.author_id = post_books.json()["author"]["id"]
        post_books.raise_for_status()
        assert post_books.status_code == 201
        assert post_books.json() == {
            "id": self.book_id,
            "name": "TestBook",
            "author": {"id": self.author_id, "name": f"{self.author_name}"},
            "genre": "TestGenre",
            "publication_date": "2000-10-10",
        }

    @staticmethod
    def test_incorrect_create_book():
        post_books = requests.post(
            API_URL + f"/books/",
            json={
                "name": "",
                "author": {"name": ""},
                "genre": "sd",
                "publication_date": "20020-10-10",
            },
        )
        assert post_books.status_code == 400

    @staticmethod
    def test_incorrect_request_create_book():
        post_books = requests.post(
            API_URL + f"/books/",
            json={"noname": "Bookname"},
        )
        assert post_books.status_code == 400

    def test_get_books_by_id(self):
        self.test_create_book()
        get_books = requests.get(API_URL + f"/books/{self.book_id}")
        get_books.raise_for_status()
        assert get_books.status_code == 200

    @staticmethod
    def test_get_books_by_incorrect_id():
        get_books = requests.get(API_URL + f"/books/sad")
        assert get_books.status_code == 404

    def test_filter_name_book(self):
        name_filter = requests.get(
            API_URL + f"/books/?name={self.filter_books()['name']}"
        )
        name_filter.raise_for_status()
        assert name_filter.status_code == 200
        assert any(item["name"] == "TestBook" for item in name_filter.json())

    def test_filter_author_book(self):
        author_filter = requests.get(
            API_URL + f"/books/?author__name={self.filter_books()['author']['name']}"
        )
        author_filter.raise_for_status()
        assert author_filter.status_code == 200
        assert any(
            item["author"]["name"] == self.author_name for item in author_filter.json()
        )

    def test_filter_genre_book(self):
        genre_filter = requests.get(
            API_URL + f"/books/?genre={self.filter_books()['genre']}"
        )
        genre_filter.raise_for_status()
        assert genre_filter.status_code == 200
        assert any(item["genre"] == "TestGenre" for item in genre_filter.json())

    def test_filter_publication_date_book(self):
        publication_date_filter = requests.get(
            API_URL
            + f"/books/?publication_date={self.filter_books()['publication_date']}"
        )
        publication_date_filter.raise_for_status()
        assert publication_date_filter.status_code == 200
        assert any(
            item["publication_date"] == "2000-10-10"
            for item in publication_date_filter.json()
        )

    def test_filter_publication_date_year_book(self):
        self.filter_books()
        publication_date_filter = requests.get(
            API_URL + f"/books/?publication_date__year=2000"
        )
        publication_date_filter.raise_for_status()
        assert publication_date_filter.status_code == 200
        assert any(
            item["publication_date"].split("-")[0] == "2000"
            for item in publication_date_filter.json()
        )

    def test_filter_publication_date_month_book(self):
        self.filter_books()
        publication_date_filter = requests.get(
            API_URL + f"/books/?publication_date__month=10"
        )
        publication_date_filter.raise_for_status()
        assert publication_date_filter.status_code == 200
        assert any(
            item["publication_date"].split("-")[1] == "10"
            for item in publication_date_filter.json()
        )

    def test_filter_publication_date_day_book(self):
        self.filter_books()
        publication_date_filter = requests.get(
            API_URL + f"/books/?publication_date__day=10"
        )
        publication_date_filter.raise_for_status()
        assert publication_date_filter.status_code == 200
        assert any(
            item["publication_date"].split("-")[2] == "10"
            for item in publication_date_filter.json()
        )

    def test_empy_filter_name_book(self):
        name_filter = requests.get(
            API_URL + f"/books/?name=incorrectnamebookincorrectnamebook"
        )
        name_filter.raise_for_status()
        assert name_filter.status_code == 200
        assert name_filter.json() == []

    def test_edit_book(self):
        self.test_create_book()
        edit_book = requests.put(
            API_URL + f"/books/{self.book_id}",
            json={
                "author": {"name": "TestAuthorName"},
                "name": "EditNameBook",
                "genre": "EditGenre",
                "publication_date": "2011-03-19",
            },
        )
        edit_book.raise_for_status()
        assert edit_book.status_code == 200
        assert edit_book.json()["name"] == "EditNameBook"
        assert edit_book.json()["author"]["name"] == "TestAuthorName"
        assert edit_book.json()["genre"] == "EditGenre"
        assert edit_book.json()["publication_date"] == "2011-03-19"

    def test_incorrect_edit_book(self):
        self.test_create_book()
        edit_book = requests.put(API_URL + f"/books/{self.book_id}", json={})
        assert edit_book.status_code == 400

    def test_delete_books_by_id(self):
        self.test_create_book()
        delete_book = requests.delete(API_URL + f"/books/{self.book_id}")
        delete_book.raise_for_status()
        assert delete_book.status_code == 204
        get_by_id = requests.get(API_URL + f"/books/{self.book_id}")
        assert get_by_id.status_code == 404
        self.book_id = None

    def test_delete_books_by_incorrect_id(self):
        self.test_create_book()
        delete_book = requests.delete(API_URL + f"/books/sdas")
        assert delete_book.status_code == 404
