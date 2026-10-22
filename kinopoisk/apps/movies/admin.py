from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Genre, Country, Movie, Season, Episode


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']


class SeasonInline(admin.TabularInline):
    model = Season
    extra = 0


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'type', 'is_active']
    list_filter = ['type', 'year', 'is_active', 'genres']
    search_fields = ['title', 'original_title']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['genres', 'countries']
    inlines = [SeasonInline]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['series', 'number', 'title']
    inlines = [EpisodeInline]
