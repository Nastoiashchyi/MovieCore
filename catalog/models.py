from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "genres"
        verbose_name = "genre"

    def __str__(self):
        return self.name


class Director(AbstractUser):
    license_card = models.CharField(max_length=8, unique=True, blank=True)

    class Meta:
        ordering = ["username"]
        verbose_name_plural = "directors"
        verbose_name = "director"

    def get_absolute_url(self):
        return reverse("catalog:director_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name_plural = "actors"
        verbose_name = "actor"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField()
    genres = models.ManyToManyField(Genre)
    directors = models.ManyToManyField(Director, blank=True)
    actors = models.ManyToManyField(Actor, through="Role", related_name="movies")

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "movies"
        verbose_name = "movie"

    def __str__(self):
        return self.title


class Role(models.Model):
    character_name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="roles")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="roles")

    def __str__(self):
        return f"{self.character_name} ({self.actor}) in {self.movie}"
