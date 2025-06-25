from django.urls import path

from catalog.views import (
    index,
    GenreListView,
    MovieListView,
    ActorListView,
    DirectorListView,
    ActorDetailView,
    MovieDetailView,
    DirectorDetailView,
    GenreDetailView,
    no_license_view,
    MovieCreateView,
    DirectorUpdateView,
    RegisterDirectorView,
    ActorCreateView,
    MovieUpdateView,
    GenreCreateView,
    GenreDeleteView,
    ActorDeleteView,
    MovieDeleteView,
    DirectorDeleteView, ToggleDirectorView,
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", RegisterDirectorView.as_view(), name="register_director"),
    path("no-license/", no_license_view, name="no_license"),
    # Genres
    path("genres/", GenreListView.as_view(), name="genre_list"),
    path("genres/<int:pk>/", GenreDetailView.as_view(), name="genre_detail"),
    path("genres/create/", GenreCreateView.as_view(), name="genre_create"),
    path("genres/<int:pk>/delete/", GenreDeleteView.as_view(), name="genre_delete"),
    # Movies
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path(
        "movies/<int:pk>/toggle-director/",
        ToggleDirectorView.as_view(),
        name="toggle_director"),
    path("movies/<int:pk>/update/", MovieUpdateView.as_view(), name="movie_update"),
    path("movies/<int:pk>/delete/", MovieDeleteView.as_view(), name="movie_delete"),
    path("movies/create/", MovieCreateView.as_view(), name="movie_create"),
    # Actors
    path("actors/", ActorListView.as_view(), name="actor_list"),
    path("actors/<int:pk>/", ActorDetailView.as_view(), name="actor_detail"),
    path("actors/create/", ActorCreateView.as_view(), name="actor_create"),
    path("actors/<int:pk>/delete/", ActorDeleteView.as_view(), name="actor_delete"),
    # Directors
    path("directors/", DirectorListView.as_view(), name="director_list"),
    path("directors/<int:pk>/", DirectorDetailView.as_view(), name="director_detail"),
    path(
        "directors/<int:pk>/update/",
        DirectorUpdateView.as_view(),
        name="director_update",
    ),
    path(
        "directors/<int:pk>/delete/",
        DirectorDeleteView.as_view(),
        name="director_delete",
    ),
]

app_name = "catalog"
