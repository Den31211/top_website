from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.movies.models import Movie
from apps.persons.models import Person
from apps.news.models import News
from .serializers import SearchResultSerializer


class SearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'results': []})

        results = []

        # Фильмы
        movies = Movie.objects.filter(
            Q(title__icontains=query) | Q(original_title__icontains=query),
            is_active=True,
        )[:20]
        for m in movies:
            results.append({
                'type': 'movie',
                'id': m.id,
                'title': m.title,
                'url': f'/movies/{m.slug}/',
                'poster': m.poster,
            })

        # Персоны
        persons = Person.objects.filter(name__icontains=query)[:20]
        for p in persons:
            results.append({
                'type': 'person',
                'id': p.id,
                'title': p.name,
                'url': f'/persons/{p.slug}/',
                'poster': p.photo,
            })

        # Новости
        news = News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query),
            is_published=True,
        )[:20]
        for n in news:
            results.append({
                'type': 'news',
                'id': n.id,
                'title': n.title,
                'url': f'/news/{n.slug}/',
                'poster': n.cover,
            })

        serializer = SearchResultSerializer(results, many=True, context={'request': request})
        return Response({'query': query, 'count': len(results), 'results': serializer.data})
