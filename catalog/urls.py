from django.urls import path

from catalog.views import index, GenreListView, MovieListView, ActorListView, DirectorListView

urlpatterns = [
    path("", index, name="index"),
    path("genres/", GenreListView.as_view(), name="genre_list" ),
    path("movies/", MovieListView.as_view(), name="movie_list" ),
    path("actors/", ActorListView.as_view(), name="actor_list" ),
    path("directors/", DirectorListView.as_view(), name="director_list" ),
]

app_name = "catalog"
