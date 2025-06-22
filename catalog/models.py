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

    class Meta:
        ordering = ["username"]


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
    director = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, through="Role")

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
