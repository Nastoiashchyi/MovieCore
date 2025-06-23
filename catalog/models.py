from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Director(AbstractUser):
    license_card = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField()
    genres = models.ManyToManyField(Genre)
    directors = models.ManyToManyField(Director, blank=True, related_name="movies")
    actors = models.ManyToManyField(Actor, through="Role", related_name="movies")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Role(models.Model):
    character_name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.character_name} ({self.actor}) in {self.movie}"
