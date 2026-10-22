from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg

from .models import Movie, Genre, Country, Season
from .serializers import (
    MovieListSerializer, MovieDetailSerializer,
    GenreSerializer, CountrySerializer, SeasonSerializer,
)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = (
        Movie.objects
        .filter(is_active=True)
        .annotate(rating_avg=Avg('ratings__score'))
        .prefetch_related('genres', 'countries', 'roles__person')
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'original_title', 'description']
    ordering_fields = ['year', 'title', 'rating_avg']
    ordering = ['-year']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # Пример фильтрации: /api/movies/?type=series&year=2024
        movie_type = self.request.query_params.get('type')
        year = self.request.query_params.get('year')
        genre = self.request.query_params.get('genre')

        if movie_type in ('movie', 'series'):
            qs = qs.filter(type=movie_type)
        if year:
            qs = qs.filter(year=year)
        if genre:
            qs = qs.filter(genres__slug=genre)
        return qs.distinct()

    @action(detail=True, methods=['get'])
    def seasons(self, request, slug=None):
        """GET /api/movies/{slug}/seasons/ — сезоны сериала."""
        movie = self.get_object()
        seasons = movie.seasons.all()
        serializer = SeasonSerializer(seasons, many=True)
        return Response(serializer.data)
