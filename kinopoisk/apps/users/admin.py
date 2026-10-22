from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Настройки отображения списка пользователей в админке
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)