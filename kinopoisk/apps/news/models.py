from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class News(models.Model):
    """Новость или статья о кино."""

    title = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField(unique=True)
    cover = models.ImageField('Обложка', upload_to='news/', blank=True)
    body = models.TextField('Текст')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news',
        verbose_name='Автор',
    )

    is_published = models.BooleanField('Опубликовано', default=True)
    published_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']

    def __str__(self):
        return self.title
