from django.contrib import admin
from django.contrib import admin
from .models import MovieList, MovieListItem
# Register your models here.



class MovieListItemInline(admin.TabularInline):
    model = MovieListItem
    extra = 1


@admin.register(MovieList)
class MovieListAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'is_public', 'created_at']
    list_filter = ['is_public']
    search_fields = ['title', 'owner__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MovieListItemInline]


@admin.register(MovieListItem)
class MovieListItemAdmin(admin.ModelAdmin):
    list_display = ['movie', 'movie_list', 'position', 'added_at']

