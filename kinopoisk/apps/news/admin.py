from django.contrib import admin
from django.contrib import admin
from .models import News
# Register your models here.



@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at']
    list_filter = ['is_published']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
