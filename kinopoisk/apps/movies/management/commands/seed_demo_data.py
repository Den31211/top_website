from django.core.management.base import BaseCommand
from django.db import transaction

from apps.movies.models import Country, Episode, Genre, Movie, Season


class Command(BaseCommand):
    help = 'Create or update fictional demo catalog entries.'

    genres = [
        ('Драма', 'drama'),
        ('Фантастика', 'science-fiction'),
        ('Детектив', 'mystery'),
        ('Приключения', 'adventure'),
        ('Триллер', 'thriller'),
    ]

    countries = ['Россия', 'Казахстан', 'Канада']

    movies = [
        {
            'slug': 'night-archive',
            'title': 'Ночной архив',
            'original_title': 'The Night Archive',
            'type': 'movie',
            'year': 2024,
            'description': 'Архивистка находит записи, предсказывающие события следующего дня.',
            'duration': 112,
            'genres': ['Драма', 'Детектив'],
            'countries': ['Россия'],
        },
        {
            'slug': 'city-above-clouds',
            'title': 'Город над облаками',
            'original_title': 'City Above the Clouds',
            'type': 'movie',
            'year': 2023,
            'description': 'Пилот исследовательского дирижабля ищет путь к затерянному городу.',
            'duration': 126,
            'genres': ['Приключения', 'Фантастика'],
            'countries': ['Казахстан'],
        },
        {
            'slug': 'last-signal',
            'title': 'Последний сигнал',
            'original_title': 'The Last Signal',
            'type': 'series',
            'year': 2025,
            'description': 'Команда полярной станции получает радиосообщение из будущего.',
            'duration': None,
            'genres': ['Фантастика', 'Триллер'],
            'countries': ['Россия', 'Канада'],
            'seasons': [
                {
                    'number': 1,
                    'title': 'Белый шум',
                    'episodes': ['Прибытие', 'Частота 19', 'За горизонтом'],
                },
                {
                    'number': 2,
                    'title': 'Ответ',
                    'episodes': ['Точка возврата', 'Тихая орбита'],
                },
            ],
        },
        {
            'slug': 'glass-harbor',
            'title': 'Стеклянная гавань',
            'original_title': 'Glass Harbor',
            'type': 'series',
            'year': 2022,
            'description': 'Следователь возвращается в приморский город, где исчезают старые дела.',
            'duration': None,
            'genres': ['Драма', 'Детектив'],
            'countries': ['Канада'],
            'seasons': [
                {
                    'number': 1,
                    'title': 'Прилив',
                    'episodes': ['Возвращение', 'Маяк', 'Низкая вода'],
                },
            ],
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        genre_objects = {}
        for name, slug in self.genres:
            genre_objects[name], _ = Genre.objects.update_or_create(
                slug=slug,
                defaults={'name': name},
            )

        country_objects = {}
        for name in self.countries:
            country_objects[name], _ = Country.objects.get_or_create(name=name)

        for item in self.movies:
            movie_data = {
                key: value
                for key, value in item.items()
                if key in {
                    'title', 'original_title', 'type', 'year',
                    'description', 'duration',
                }
            }
            movie, _ = Movie.objects.update_or_create(
                slug=item['slug'],
                defaults=movie_data,
            )
            movie.genres.set(genre_objects[name] for name in item['genres'])
            movie.countries.set(country_objects[name] for name in item['countries'])

            for season_data in item.get('seasons', []):
                season, _ = Season.objects.update_or_create(
                    series=movie,
                    number=season_data['number'],
                    defaults={'title': season_data['title']},
                )
                for number, title in enumerate(season_data['episodes'], start=1):
                    Episode.objects.update_or_create(
                        season=season,
                        number=number,
                        defaults={'title': title, 'duration': 45},
                    )

        self.stdout.write(self.style.SUCCESS(
            'Demo catalog ready: '
            f'{Genre.objects.count()} genres, '
            f'{Country.objects.count()} countries, '
            f'{Movie.objects.count()} movies/series, '
            f'{Season.objects.count()} seasons, '
            f'{Episode.objects.count()} episodes.'
        ))
