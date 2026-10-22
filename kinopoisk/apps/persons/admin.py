from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Person, Role


class RoleInline(admin.TabularInline):
    model = Role
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'birth_date']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RoleInline]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['person', 'movie', 'role_type', 'character_name']
    list_filter = ['role_type']
