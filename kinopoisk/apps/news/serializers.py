from rest_framework import serializers
from .models import News


class NewsListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = News
        # TODO: при необходимости добавьте 'author'
        fields = ['id', 'title', 'slug', 'cover', 'published_at', 'author']


class NewsDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = News
        # TODO: дополните список (id, title, slug, cover, body, author, published_at)
        fields = ['id', 'title', 'slug', 'cover', 'body', 'author', 'published_at']

