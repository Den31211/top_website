from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Rating, Review


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'score', 'created_at']
    list_filter = ['score']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'is_spoiler', 'created_at']
    list_filter = ['is_spoiler']
