import django_filters
from rest_framework.exceptions import ValidationError

from .models import Author, Book


class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Author
        fields = ["name"]


class BookFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    author__name = django_filters.CharFilter(lookup_expr="icontains")
    genre = django_filters.CharFilter(lookup_expr="icontains")
    publication_date = django_filters.DateFilter()
    publication_date__year = django_filters.NumberFilter(
        field_name="publication_date", lookup_expr="year"
    )
    publication_date__day = django_filters.NumberFilter(
        method="filter_publication_date_day", lookup_expr="day"
    )
    publication_date__month = django_filters.NumberFilter(
        method="filter_publication_date_month", lookup_expr="month"
    )

    @staticmethod
    def filter_publication_date_day(queryset, name, value):
        if 1 <= value <= 31:
            return queryset.filter(publication_date__day=value)
        else:
            raise ValidationError(
                "Invalid day. Please enter a number between 1 and 31."
            )

    @staticmethod
    def filter_publication_date_month(queryset, name, value):
        if 1 <= value <= 12:
            return queryset.filter(publication_date__month=value)
        else:
            raise ValidationError(
                "Invalid month. Please enter a number between 1 and 12."
            )

    class Meta:
        model = Book
        fields = ["name", "author", "genre", "publication_date"]
