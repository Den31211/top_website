from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.movies.models import Genre, Movie
from apps.ratings.models import Rating


class CatalogPageTests(TestCase):
	def setUp(self):
		self.drama = Genre.objects.create(name='Драма', slug='drama')
		self.movie = Movie.objects.create(
			title='Тихий берег',
			original_title='Quiet Shore',
			slug='quiet-shore',
			type='movie',
			year=2024,
			description='История маленького приморского города.',
		)
		self.movie.genres.add(self.drama)
		Movie.objects.create(
			title='Северный свет',
			original_title='Northern Light',
			slug='northern-light',
			type='series',
			year=2023,
			description='Команда исследователей отправляется на север.',
		)

	def test_homepage_shows_catalog(self):
		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Тихий берег')
		self.assertContains(response, 'Северный свет')

	def test_homepage_filters_by_search_type_and_genre(self):
		response = self.client.get(reverse('home'), {
			'q': 'тихий',
			'type': 'movie',
			'genre': 'drama',
		})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Тихий берег')
		self.assertNotContains(response, 'Северный свет')

	def test_detail_page_shows_movie_information(self):
		response = self.client.get(reverse('web-movie-detail', args=[self.movie.slug]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Тихий берег')
		self.assertContains(response, 'История маленького приморского города.')

	def test_registration_creates_and_logs_in_user(self):
		response = self.client.post(reverse('account-register'), {
			'username': 'viewer',
			'password1': 'StrongTestPass123!',
			'password2': 'StrongTestPass123!',
			'email': 'viewer@example.com',
		})

		self.assertRedirects(response, reverse('home'))
		self.assertTrue(get_user_model().objects.filter(username='viewer').exists())
		self.assertIn('_auth_user_id', self.client.session)

	def test_login_authenticates_existing_user(self):
		get_user_model().objects.create_user(
			username='returning-viewer',
			email='returning@example.com',
			password='StrongTestPass123!',
		)

		response = self.client.post(reverse('account-login'), {
			'username': 'returning@example.com',
			'password': 'StrongTestPass123!',
		})

		self.assertRedirects(response, reverse('home'))
		self.assertIn('_auth_user_id', self.client.session)

	def test_authenticated_user_can_rate_movie(self):
		user = get_user_model().objects.create_user(
			username='rater',
			password='StrongTestPass123!',
		)
		self.client.force_login(user)

		response = self.client.post(reverse('rate-movie', args=[self.movie.slug]), {'score': '8'})

		self.assertRedirects(response, reverse('web-movie-detail', args=[self.movie.slug]))
		self.assertEqual(Rating.objects.get(user=user, movie=self.movie).score, 8)

# Create your tests here.
