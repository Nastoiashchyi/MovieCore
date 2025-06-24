from django.urls import path

from catalog.views import index, GenreListView, MovieListView, ActorListView, DirectorListView, ActorDetailView, \
    MovieDetailView, DirectorDetailView, GenreDetailView, toggle_director, \
    no_license_view, MovieCreateView, DirectorUpdateView, RegisterDirectorView

urlpatterns = [
    path("", index, name="index"),
    path("genres/", GenreListView.as_view(), name="genre_list" ),
    path("genres/<int:pk>/", GenreDetailView.as_view(), name="genre_detail"),

    path("movies/", MovieListView.as_view(), name="movie_list" ),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("movies/<int:pk>/toggle-director/", toggle_director, name="toggle_director"),

    path("actors/", ActorListView.as_view(), name="actor_list" ),
    path("actors/<int:pk>/", ActorDetailView.as_view(), name="actor_detail" ),

    path("directors/", DirectorListView.as_view(), name="director_list" ),
    path("directors/<int:pk>/", DirectorDetailView.as_view(), name="director_detail"),
    path("directors/<int:pk>/update/", DirectorUpdateView.as_view(), name="director_update"),

    path("register/", RegisterDirectorView.as_view(), name="register_director"),
    path("movies/create/", MovieCreateView.as_view(), name="movie_create"),
    path("no-license/", no_license_view, name="no_license"),

]

app_name = "catalog"
