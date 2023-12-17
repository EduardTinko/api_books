from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="book")
    genre = models.CharField(max_length=50)
    publication_date = models.DateField()
