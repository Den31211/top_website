from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
class Film(models.Model):
    TYPE_CHOICES = [
        ('movie','фильм'),
        ('series', 'сериал'),
    ]
    slug = models.SlugField(unique=True,verbose_name='ссылка')
    rating = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='movie')
    name = models.CharField('Название', max_length=300, unique=True)
    genre = models.ManyToManyField('Genre', related_name='films')
    relise_year = models.PositiveIntegerField('Год')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Movie(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Фильм'),
        ('series', 'Сериал'),
        ('cartoon', 'Мультфильм'),
    ]
    title = models.CharField('Название', max_length=255)
    original_title = models.CharField('Оригинальное название', max_length=255, blank=True)
    slug = models.SlugField(unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='movie')
    year = models.PositiveIntegerField('Год')
    description = models.TextField('Описание')
    poster = models.ImageField(upload_to='posters/', blank=True)
    trailer_url = models.URLField(blank=True)
    genres = models.ManyToManyField('Genre', related_name='movies')
    countries = models.ManyToManyField(Country, related_name='movies')
    duration = models.PositiveIntegerField('Длительность (мин)', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Фильм/Сериал'
        verbose_name_plural = 'Фильмы и сериалы'
        ordering = ['-year']
    def __str__(self):
        return f'{self.title} ({self.year})'
class Season(models.Model):
    series = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons', limit_choices_to={'type': 'series'})
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('series', 'number')
        ordering = ['number']

    def __str__(self):
        return f'{self.series} — Сезон {self.number}'
class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    duration = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('season', 'number')
        ordering = ['number']


