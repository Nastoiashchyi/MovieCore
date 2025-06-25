import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.forms import DirectorSignUpForm
from catalog.models import Genre, Movie, Actor


class DirectorSignUpFormTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.User.objects.create_user(
            username="existing", password="testpass123", license_card="AB123456"
        )

    def test_valid_license_card_format(self):
        form_data = {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Eva",
            "last_name": "Green",
            "email": "eva@example.com",
            "license_card": "CD789012",
        }
        form = DirectorSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_card_format(self):
        form_data = {
            "username": "invaliduser",
            "password1": "Pass12345!",
            "password2": "Pass12345!",
            "first_name": "Tom",
            "last_name": "Hardy",
            "email": "tom@example.com",
            "license_card": "cd78",  # ❌ неправильний формат
        }
        form = DirectorSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_card", form.errors)
        self.assertIn("format should be", form.errors["license_card"][0])

    def test_duplicate_license_card(self):
        form_data = {
            "username": "anotheruser",
            "password1": "AnotherPass123!",
            "password2": "AnotherPass123!",
            "first_name": "Chris",
            "last_name": "Nolan",
            "email": "chris@example.com",
            "license_card": "AB123456",  # ❌ уже існує в базі
        }
        form = DirectorSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_card", form.errors)
        self.assertIn("already in use", form.errors["license_card"][0])


class GenreListViewSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("user", password="pass")
        self.client.login(username="user", password="pass")
        Genre.objects.create(name="Drama")
        Genre.objects.create(name="Comedy")
        Genre.objects.create(name="Thriller")

    def test_genre_search(self):
        response = self.client.get(reverse("catalog:genre_list"), {"q": "com"})
        self.assertContains(response, "Comedy")
        self.assertNotContains(response, "Drama")
        self.assertNotContains(response, "Thriller")


class MovieListViewSearchTest(TestCase):
    def setUp(self):
        self.director = get_user_model().objects.create_user(
            "dir", password="pass", license_card="LC123456"
        )
        self.client.login(username="dir", password="pass")
        Movie.objects.create(title="Inception", release_date="2010-07-16", rating=8.8)
        Movie.objects.create(title="Dunkirk", release_date="2017-07-21", rating=7.9)

    def test_movie_search(self):
        response = self.client.get(reverse("catalog:movie_list"), {"q": "incep"})
        self.assertContains(response, "Inception")
        self.assertNotContains(response, "Dunkirk")


class ActorListViewSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("viewer", password="pass")
        self.client.login(username="viewer", password="pass")
        Actor.objects.create(first_name="Emma", last_name="Stone")
        Actor.objects.create(first_name="Ryan", last_name="Gosling")

    def test_actor_search(self):
        response = self.client.get(reverse("catalog:actor_list"), {"q": "ryan"})
        self.assertContains(response, "Ryan Gosling")
        self.assertNotContains(response, "Emma Stone")


class DirectorListViewSearchTest(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            "admin", password="pass"
        )
        self.client.login(username="admin", password="pass")
        get_user_model().objects.create_user(
            username="nolan",
            first_name="Chris",
            last_name="Nolan",
            password="pass",
            license_card="LC0001",
        )
        get_user_model().objects.create_user(
            username="taika",
            first_name="Taika",
            last_name="Waititi",
            password="pass",
            license_card="LC0002",
        )

    def test_director_search(self):
        response = self.client.get(reverse("catalog:director_list"), {"q": "wait"})
        self.assertContains(response, "Taika Waititi")
        self.assertNotContains(response, "Chris Nolan")


class NavigationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="pass", license_card="LC000001"
        )
        self.client.login(username="testuser", password="pass")
        self.genre = Genre.objects.create(name="Drama")
        self.actor = Actor.objects.create(first_name="Emma", last_name="Stone")
        self.movie = Movie.objects.create(
            title="TestMovie",
            description="Desc",
            release_date=datetime.date(2024, 1, 1),
            rating=8.5,
        )
        self.movie.genres.add(self.genre)
        self.movie.actors.add(self.actor)
        self.movie.directors.add(self.user)

    def test_index_redirect(self):
        response = self.client.get(reverse("catalog:index"))
        self.assertEqual(response.status_code, 200)

    def test_genre_detail_link(self):
        response = self.client.get(
            reverse("catalog:genre_detail", args=[self.genre.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.genre.name)

    def test_actor_detail_link(self):
        response = self.client.get(
            reverse("catalog:actor_detail", args=[self.actor.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.actor.first_name)

    def test_movie_detail_link(self):
        response = self.client.get(
            reverse("catalog:movie_detail", args=[self.movie.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)

    def test_director_detail_link(self):
        response = self.client.get(
            reverse("catalog:director_detail", args=[self.user.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.get_full_name())


class AuthLinkTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="securepass"
        )

    def test_login_page_accessible(self):
        response = self.client.get(reverse("login"))  # стандартний шлях
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")  # або щось із шаблону

    def test_logout_redirects(self):
        self.client.login(username="tester", password="securepass")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have successfully exit")

    def test_register_director_page_accessible(self):
        response = self.client.get(reverse("catalog:register_director"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")  # або вміст шаблону

    def test_register_form_submission_valid(self):
        form_data = {
            "username": "newuser",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "license_card": "AA123456",
        }
        response = self.client.post(
            reverse("catalog:register_director"), data=form_data
        )
        self.assertEqual(response.status_code, 302)  # редірект після успіху


class ToggleDirectorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="dir", password="pass", license_card="LC123456"
        )
        self.client.login(username="dir", password="pass")
        self.movie = Movie.objects.create(
            title="Test", release_date="2024-01-01", rating=8
        )

    def test_toggle_director_add_and_remove(self):
        url = reverse("catalog:toggle_director", args=[self.movie.pk])

        response = self.client.post(url)
        self.assertIn(self.user, self.movie.directors.all())

        response = self.client.post(url)
        self.movie.refresh_from_db()
        self.assertNotIn(self.user, self.movie.directors.all())
