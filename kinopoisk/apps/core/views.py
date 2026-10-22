from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Avg, Q
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from apps.users.forms import CustomUserCreationForm 
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model
from apps.movies.models import Genre, Movie
from apps.ratings.models import Rating, Review


# Create your views here.


def home(request):
    movies = Movie.objects.filter(is_active=True).annotate(
        rating_avg=Avg('ratings__score')
    ).prefetch_related('genres', 'countries')

    query = request.GET.get('q', '').strip()
    movie_type = request.GET.get('type', '')
    genre_slug = request.GET.get('genre', '')
    ordering = request.GET.get('sort', 'newest')

    if query:
        if connection.vendor == 'sqlite' and not query.isascii():
            folded_query = query.casefold()
            matching_ids = [
                movie_id
                for movie_id, title, original_title, description in movies.values_list(
                    'id', 'title', 'original_title', 'description'
                )
                if folded_query in ' '.join((title, original_title, description)).casefold()
            ]
            movies = movies.filter(pk__in=matching_ids)
        else:
            movies = movies.filter(
                Q(title__icontains=query)
                | Q(original_title__icontains=query)
                | Q(description__icontains=query)
            )
    if movie_type in ('movie', 'series', 'cartoon'):
        movies = movies.filter(type=movie_type)
    if genre_slug:
        movies = movies.filter(genres__slug=genre_slug)

    ordering_options = {
        'newest': ('-year', 'title'),
        'oldest': ('year', 'title'),
        'title': ('title',),
        'rating': ('-rating_avg', '-year'),
    }
    movies = movies.order_by(*ordering_options.get(ordering, ordering_options['newest']))

    page_obj = Paginator(movies.distinct(), 12).get_page(request.GET.get('page'))
    return render(request, 'core/home.html', {
        'page_obj': page_obj,
        'genres': Genre.objects.order_by('name'),
        'query': query,
        'selected_type': movie_type,
        'selected_genre': genre_slug,
        'selected_sort': ordering if ordering in ordering_options else 'newest',
        'movie_count': Movie.objects.filter(is_active=True, type='movie').count(),
        'series_count': Movie.objects.filter(is_active=True, type='series').count(),
        'cartoon_count': Movie.objects.filter(is_active=True, type='cartoon').count(),
    })


def movie_detail(request, slug):
    movie = get_object_or_404(
        Movie.objects.filter(is_active=True)
        .annotate(rating_avg=Avg('ratings__score'))
        .prefetch_related('genres', 'countries', 'roles__person', 'seasons__episodes'),
        slug=slug,
    )
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, movie=movie).values_list(
            'score', flat=True
        ).first()
    return render(request, 'core/movie_detail.html', {
        'movie': movie,
        'user_rating': user_rating,
        'rating_choices': range(1, 11),
    })


def account_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'core/account.html', {
        'form': form,
        'page_title': 'Вход',
        'submit_label': 'Войти',
        'alternate_text': 'Ещё нет аккаунта?',
        'alternate_label': 'Зарегистрироваться',
        'alternate_url': 'account-register',
    })


def account_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'core/account.html', {
        'form': form,
        'page_title': 'Регистрация',
        'submit_label': 'Создать аккаунт',
        'alternate_text': 'Уже есть аккаунт?',
        'alternate_label': 'Войти',
        'alternate_url': 'account-login',
    })


@login_required(login_url='account-login')
@require_POST
def rate_movie(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    try:
        score = int(request.POST.get('score', ''))
    except (TypeError, ValueError):
        score = 0

    if not 1 <= score <= 10:
        messages.error(request, 'Оценка должна быть от 1 до 10.')
    else:
        Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'score': score},
        )
        messages.success(request, 'Ваша оценка сохранена.')
    return redirect('web-movie-detail', slug=slug)


@login_required(login_url='account-login')
@require_POST
def account_logout(request):
    logout(request)
    return redirect('home')



class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'status': 'ok'})


class APIRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'project': 'kinopoisk',
            'status': 'ok',
            'endpoints': {
                'health': '/api/core/health/',
                'stats': '/api/core/stats/',
                'movies': '/api/movies/',
                'users': '/api/users/',
                'persons': '/api/persons/',
                'ratings': '/api/ratings/',
                'lists': '/api/lists/',
                'news': '/api/news/',
                'search': '/api/search/',
            }
        })


class StatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        User = get_user_model()
        return Response({
            'movies_count': Movie.objects.filter(is_active=True).count(),
            'users_count': User.objects.count(),
            'ratings_count': Rating.objects.count(),
            'reviews_count': Review.objects.count(),
        })
