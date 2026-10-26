from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import MovieList, MovieListItem
from .serializers import MovieListSerializer, MovieListItemSerializer
from django.db.models import Q, QuerySet
# Create your views here.



class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsMovieListItemOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.movie_list.owner == request.user

class MovieListViewSet(viewsets.ModelViewSet):
    queryset = MovieList.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self) -> QuerySet[MovieList]: # pyright: ignore[reportIncompatibleMethodOverride]
        qs = MovieList.objects.select_related('owner').prefetch_related('items__movie')
        # Публичные списки — всем, свои — только владельцу
        if self.request.user.is_authenticated:
            return qs.filter(is_public=True) | qs.filter(owner=self.request.user)
        return qs.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MovieListItemViewSet(viewsets.ModelViewSet):
    queryset = MovieListItem.objects.select_related('movie', 'movie_list')
    serializer_class = MovieListItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsMovieListItemOwnerOrReadOnly,]

    def get_queryset(self) -> QuerySet[MovieListItem]: # pyright: ignore[reportIncompatibleMethodOverride]
        qs: QuerySet[MovieListItem] = MovieListItem.objects.select_related(
            'movie', 'movie_list', 'movie_list__owner'
)

        if self.request.user.is_authenticated:
            return qs.filter(
                Q(movie_list__is_public=True)
                | Q(movie_list__owner=self.request.user)
            )

        return qs.filter(movie_list__is_public=True)
