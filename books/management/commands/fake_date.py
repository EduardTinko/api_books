import random

from django.core.management.base import BaseCommand
from faker import Faker

from ...models import Author, Book

fake = Faker("uk_UA")


class Command(BaseCommand):
    def handle(self, *args, **options):
        Author.objects.all().delete()
        Book.objects.all().delete()

        for _ in range(5):
            Author.objects.create(name=fake.name())

        authors = Author.objects.all()

        for author in authors:
            k = random.randint(1, 3)
            for _ in range(k):
                random_publication_date = fake.date_between(start_date='-20y', end_date='today')
                formatted_date = random_publication_date.strftime("%Y-%m-%d")
                Book.objects.create(
                    name=fake.catch_phrase(),
                    author=author,
                    genre=fake.word(),
                    publication_date=formatted_date
                )

        self.stdout.write(self.style.SUCCESS("Базу даних успішно заповнено"))