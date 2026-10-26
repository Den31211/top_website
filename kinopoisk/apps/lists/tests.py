from apps.users.models import CustomUser as User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.lists.models import MovieList, MovieListItem
from apps.movies.models import Movie


class MovieListItemPermissionsTests(APITestCase):
    client_class = APIClient
    api_client: APIClient
    def setUp(self):
        self.client = APIClient()

        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123',
        )
        self.other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='testpass123',
        )

        self.movie = Movie.objects.create(
            title='Первый фильм',
            slug='first-test-movie',
            year=2020,
            description='Тестовый фильм',
        )
        self.another_movie = Movie.objects.create(
            title='Второй фильм',
            slug='second-test-movie',
            year=2021,
            description='Ещё один тестовый фильм',
        )

        self.public_list = MovieList.objects.create(
            title='Публичная подборка',
            owner=self.owner,
            is_public=True,
        )
        self.private_list = MovieList.objects.create(
            title='Приватная подборка',
            owner=self.owner,
            is_public=False,
        )

        self.public_item = MovieListItem.objects.create(
            movie_list=self.public_list,
            movie=self.movie,
        )
        self.private_item = MovieListItem.objects.create(
            movie_list=self.private_list,
            movie=self.movie,
        )

        self.list_url = reverse('list-item-list')

    def item_url(self, item):
        return reverse('list-item-detail', args=[item.pk])

    def test_owner_can_edit_own_item(self):
        self.client.force_login(user=self.owner)

        response = self.client.patch(
            self.item_url(self.public_item),
            {'comment': 'Мой комментарий'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.public_item.refresh_from_db()
        self.assertEqual(
            self.public_item.comment,
            'Мой комментарий',
        )

    def test_other_user_cannot_edit_foreign_item(self):
        self.client.force_login(user=self.other_user)

        response = self.client.patch(
            self.item_url(self.public_item),
            {'comment': 'Чужое изменение'},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_other_user_cannot_delete_foreign_item(self):
        self.client.force_login(user=self.other_user)

        response = self.client.delete(
            self.item_url(self.public_item)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            MovieListItem.objects.filter(
                pk=self.public_item.pk
            ).exists()
        )

    def test_owner_can_add_movie_to_own_list(self):
        self.client.force_login(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                'movie_list_id': self.public_list.pk,
                'movie_id': self.another_movie.pk,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            MovieListItem.objects.filter(
                movie_list=self.public_list,
                movie=self.another_movie,
            ).exists()
        )

    def test_other_user_cannot_add_movie_to_foreign_list(self):
        self.client.force_login(user=self.other_user)

        response = self.client.post(
            self.list_url,
            {
                'movie_list_id': self.public_list.pk,
                'movie_id': self.another_movie.pk,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(
            MovieListItem.objects.filter(
                movie_list=self.public_list,
                movie=self.another_movie,
            ).exists()
        )

    def test_other_user_cannot_read_private_item(self):
        self.client.force_login(user=self.other_user)

        response = self.client.get(
            self.item_url(self.private_item)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )