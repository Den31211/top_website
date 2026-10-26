from django.db import models
from django.conf import settings
from apps.movies.models import Movie
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.



class MovieList(models.Model):
    """Пользовательский список фильмов (подборка, «избранное», топ и т.п.)."""

    title = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField(unique=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='movie_lists',
        verbose_name='Владелец',
    )

    is_public = models.BooleanField('Публичный', default=True)
    cover = models.ImageField('Обложка', upload_to='lists/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'
        ordering = ['-created_at']
        # один и тот же slug у разных пользователей не нужен — оставляем глобально уникальным
        # но если хотите разрешить одноимённые списки у разных юзеров — см. задание ниже
        unique_together = ('owner', 'title')

    def __str__(self):
        return f'{self.title} — {self.owner}'


class MovieListItem(models.Model):
    """Один фильм внутри списка."""

    movie_list = models.ForeignKey(
        MovieList,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Список',
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='in_lists',
        verbose_name='Фильм',
    )
    position = models.PositiveIntegerField('Позиция', default=0)
    comment = models.CharField('Комментарий', max_length=255, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Элемент списка'
        verbose_name_plural = 'Элементы списков'
        ordering = ['position', '-added_at']
        unique_together = ('movie_list', 'movie')   # фильм не может дважды быть в одном списке

    def __str__(self):
        return f'{self.movie} в «{self.movie_list}»'
@receiver(pre_save, sender=MovieList)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        base = slugify(instance.title, allow_unicode=True) or 'list'
        slug = base
        i = 1
        while MovieList.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            i += 1
            slug = f'{base}-{i}'
        instance.slug = slug

