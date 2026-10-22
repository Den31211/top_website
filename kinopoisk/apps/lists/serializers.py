from rest_framework import serializers
from apps.movies.serializers import MovieListSerializer as MovieShortSerializer
from .models import MovieList, MovieListItem


# ---------- Элемент списка ----------

class MovieListItemSerializer(serializers.ModelSerializer):
    movie = MovieShortSerializer(read_only=True)          # для чтения — вложенный объект
    movie_id = serializers.PrimaryKeyRelatedField(        # для записи — id фильма
        queryset=MovieShortSerializer.Meta.model.objects.all()
        if hasattr(MovieShortSerializer.Meta, 'model')
        else None,
        source='movie',
        write_only=True,
    )

    class Meta:
        model = MovieListItem
        fields = ['id', 'movie', 'movie_id', 'position', 'comment', 'added_at']
        read_only_fields = ['id', 'added_at']


# ---------- Список ----------

class MovieListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    items = MovieListItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = MovieList
        fields = [
            'id', 'title', 'slug', 'description',
            'owner', 'is_public', 'cover',
            'items', 'items_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'owner', 'created_at', 'updated_at']

    def get_items_count(self, obj):
        # TODO: вернуть количество элементов списка
        # подсказка: obj.items.count()
        return obj.items.count()