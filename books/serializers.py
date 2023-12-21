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
        author = Author.objects.filter(name=author_data["name"]).first()
        if not author:
            author = Author.objects.create(name=author_data["name"])
        book = Book.objects.create(author=author, **validated_data)
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
            author = Author.objects.filter(name=author_data["name"]).first()
            if not author:
                author = Author.objects.create(name=author_data["name"])

            instance.author = author
            instance.save()

        return instance

    class Meta:
        model = Book
        fields = ["id", "name", "author", "genre", "publication_date"]
