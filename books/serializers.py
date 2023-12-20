from rest_framework import serializers

from books.models import Author, Book


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name"]


class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer()

    def create(self, validated_data):
        author_data = validated_data.pop("author")
        author_instance = AuthorSerializer().create(author_data)
        book = Book.objects.create(author=author_instance, **validated_data)
        return book

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.genre = validated_data.get("genre", instance.genre)
        instance.publication_date = validated_data.get(
            "publication_date", instance.publication_date
        )
        instance.save()

        author_data = validated_data.get("author")
        if author_data:
            author_name = author_data.get("name")
            author, created = Author.objects.get_or_create(name=author_name)

            if not created:
                author.name = author_data.get("name", author.name)
                author.save()

            instance.author = author
            instance.save()

        return instance

    class Meta:
        model = Book
        fields = ["name", "author", "genre", "publication_date"]
