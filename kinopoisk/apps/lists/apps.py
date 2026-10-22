from django.apps import AppConfig


class ListsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lists'          # ← должно быть именно так, с префиксом apps.

