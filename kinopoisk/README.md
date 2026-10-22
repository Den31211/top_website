# Kinopoisk API

Этот проект представляет собой Django REST API для каталога фильмов, сериалов, новостей, списков, рейтингов и пользователей.

## Стек

- Python 3.9+
- Django 4.2 LTS
- Django REST Framework
- SQLite по умолчанию

## Быстрый старт

1. Создайте виртуальное окружение:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Примените миграции:

   ```bash
   python manage.py migrate
   ```

4. Запустите сервер:

   ```bash
   python manage.py runserver
   ```

5. Откройте проект:

   ```text
   http://127.0.0.1:8000/
   ```

## Переменные окружения

Скопируйте пример файла:

```bash
cp .env.example .env
```

После этого настройте значения по необходимости.

## Структура проекта

- `apps/` — Django-приложения проекта
- `kinopoisk/` — конфигурация проекта и маршруты
- `db.sqlite3` — SQLite база данных

## Важно

Если в проекте есть папка `venv` с Windows-специфичными файлами (`Scripts/...`), лучше удалить её и пересоздать окружение в macOS/Linux:

```bash
rm -rf venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Полезные команды

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
