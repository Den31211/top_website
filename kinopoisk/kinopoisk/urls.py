"""
URL configuration for kinopoisk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import (
    account_login, account_logout, account_register, home, movie_detail, rate_movie,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('title/<slug:slug>/', movie_detail, name='web-movie-detail'),
    path('account/login/', account_login, name='account-login'),
    path('account/register/', account_register, name='account-register'),
    path('account/logout/', account_logout, name='account-logout'),
    path('title/<slug:slug>/rate/', rate_movie, name='rate-movie'),
    path('api/core/', include('apps.core.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/movies/', include('apps.movies.urls')),
    path('api/persons/', include('apps.persons.urls')),
    path('api/ratings/', include('apps.ratings.urls')),
    path('api/lists/', include('apps.lists.urls')),
    path('api/news/', include('apps.news.urls')),
    path('api/search/', include('apps.search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
