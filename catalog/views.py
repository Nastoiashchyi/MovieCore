from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.views import generic

from catalog.models import Genre, Director, Movie, Actor


@login_required
def index(request):
    num_directors = Director.objects.count()
    num_movies = Movie.objects.count()
    num_actors = Actor.objects.count()
    num_genres = Genre.objects.count()
    top_movies = Movie.objects.order_by("-rating")[:3]
    top_directors = Director.objects.annotate(movie_count=Count("movie")).order_by("-movie_count", "first_name")[:3]

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_directors": num_directors,
        "num_movies": num_movies,
        "num_genres": num_genres,
        "num_actors": num_actors,
        "num_visits": num_visits + 1,
        "top_movies": top_movies,
        "top_directors": top_directors,
    }

    return render(request, "catalog/index.html", context=context)


class GenreListView(generic.ListView):
    model = Genre
    template_name = "catalog/genre_list.html"
    context_object_name = "genre_list"
    ordering = ["name"]

    def get_queryset(self):
        return Genre.objects.annotate(movie_count=Count("movie"))


class DirectorListView(generic.ListView):
    model = Director
    template_name = "catalog/director_list.html"
    context_object_name = "director_list"
    # ordering = ["first_name", "last_name"]

    def get_queryset(self):
        return Director.objects.annotate(movie_count=Count("movie"))


class ActorListView(generic.ListView):
    model = Actor
    template_name = "catalog/actor_list.html"
    context_object_name = "actor_list"
    # ordering = ["first_name"]

    def get_queryset(self):
        return Actor.objects.annotate(movie_count=Count("role__movie", distinct=True))


class MovieListView(generic.ListView):
    model = Movie
    template_name = "catalog/movie_list.html"
    context_object_name = "movie_list"
    # ordering = ["-release_date"]
