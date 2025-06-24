from django.urls import path

from catalog.views import index, GenreListView, MovieListView, ActorListView, DirectorListView, ActorDetailView, \
    MovieDetailView, DirectorDetailView, GenreDetailView

urlpatterns = [
    path("", index, name="index"),
    path("genres/", GenreListView.as_view(), name="genre_list" ),
    path("genres/<int:pk>/", GenreDetailView.as_view(), name="genre_detail"),

    path("movies/", MovieListView.as_view(), name="movie_list" ),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),

    path("actors/", ActorListView.as_view(), name="actor_list" ),
    path("actors/<int:pk>/", ActorDetailView.as_view(), name="actor_detail" ),

    path("directors/", DirectorListView.as_view(), name="director_list" ),
    path("directors/<int:pk>/", DirectorDetailView.as_view(), name="director_detail"),

]

app_name = "catalog"
