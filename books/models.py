from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


def validate_name(value):
    if len(value) <= 1:
        raise ValidationError(f"Value is too short.")


class Author(models.Model):
    name = models.CharField(max_length=100, validators=[validate_name])


class Book(models.Model):
    name = models.CharField(max_length=100, validators=[validate_name])
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="book")
    genre = models.CharField(max_length=50, validators=[validate_name])
    publication_date = models.DateField()
