from django.db import models
from apps.movies.models import Movie
# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(upload_to='persons/', blank=True)
    birth_date = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    ROLE_TYPES = [
        ('actor', 'Актёр'),
        ('director', 'Режиссёр'),
        ('writer', 'Сценарист'),
    ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='roles')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='roles')
    role_type = models.CharField(max_length=20, choices=ROLE_TYPES)
    character_name = models.CharField('Роль', max_length=150, blank=True)

    class Meta:
        unique_together = ('movie', 'person', 'role_type')
