from rest_framework import serializers
from .models import Movie, Genre, Season, Episode, Country
from apps.persons.models import Person, Role
from apps.ratings.models import Rating, Review

# ---------- Жанры и страны ----------

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        # TODO: укажите поля (id, name)
        fields = ['id', 'name']

# ---------- Персоны (краткая версия) ----------

class PersonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'slug', 'photo']


class RoleSerializer(serializers.ModelSerializer):
    person = PersonShortSerializer(read_only=True)

    class Meta:
        model = Role
        fields = ['person', 'role_type', 'character_name']

# ---------- Список фильмов ----------

class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    rating_avg = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'slug', 'year', 'poster', 'type', 'genres', 'rating_avg']

# ---------- Детальная карточка фильма ----------

class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    roles = RoleSerializer(many=True, read_only=True)
    rating_avg = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'slug', 'type', 'year',
            'description', 'poster', 'trailer_url', 'genres',
            'duration', 'roles', 'rating_avg', 'countries'
        ]

# ---------- Сезоны и эпизоды ----------

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        # TODO: укажите поля (id, number, title, duration)
        fields = ['id', 'number', 'title', 'duration']

class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)
    class Meta:
        model = Season
        # TODO: укажите поля (id, number, title, episodes)
        fields = ['id', 'number', 'title', 'episodes']

class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    rating_avg = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'slug', 'year', 'poster',
            'type', 'genres', 'rating_avg'
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    roles = RoleSerializer(many=True, read_only=True)
    rating_avg = serializers.FloatField(read_only=True, required=False)
    seasons_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'slug', 'type', 'year',
            'description', 'poster', 'trailer_url',
            'genres', 'countries', 'duration',
            'roles', 'rating_avg', 'seasons_count',
        ]

    def get_seasons_count(self, obj):
        if obj.type != 'series':
            return 0
        return obj.seasons.count()
