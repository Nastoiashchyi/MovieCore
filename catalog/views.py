from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from catalog.forms import DirectorSignUpForm, MovieCreateForm, RoleInlineFormSet, DirectorUpdateForm
from catalog.models import Genre, Director, Movie, Actor


@login_required
def index(request):
    num_directors = Director.objects.count()
    num_movies = Movie.objects.count()
    num_actors = Actor.objects.count()
    num_genres = Genre.objects.count()
    top_movies = Movie.objects.order_by("-rating")[:3]
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_directors": num_directors,
        "num_movies": num_movies,
        "num_genres": num_genres,
        "num_actors": num_actors,
        "num_visits": num_visits + 1,
        "top_movies": top_movies,
    }
    return render(request, "catalog/index.html", context=context)

#class for GENRE
class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name = "catalog/genre_list.html"
    context_object_name = "genre_list"
    paginate_by = 6

    def get_queryset(self):
        queryset = Genre.objects.annotate(
            movie_count=Count("movie")
        ).order_by("-movie_count")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class GenreDetailView(LoginRequiredMixin, generic.DetailView):
    model = Genre
    template_name = "catalog/genre_detail.html"
    context_object_name = "genre"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = Movie.objects.filter(genres=self.object)
        return context

#class for DIRECTOR
class DirectorListView(LoginRequiredMixin, generic.ListView):
    model = Director
    template_name = "catalog/director_list.html"
    context_object_name = "director_list"
    paginate_by = 6

    def get_queryset(self):
        queryset = Director.objects.annotate(
            movie_count=Count("movie")
        ).order_by("first_name", "last_name")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class DirectorUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = get_user_model()
    form_class = DirectorUpdateForm
    template_name = "catalog/director_update.html"

    def get_success_url(self):
        return reverse("catalog:director_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        # Дозволяємо редагувати самого себе або суперкористувачу
        return self.request.user == self.get_object() or self.request.user.is_superuser

class DirectorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Director
    template_name = "catalog/director_detail.html"
    context_object_name = "director"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = Movie.objects.filter(directors=self.object)
        return context

#class for ACTOR
class ActorListView(LoginRequiredMixin, generic.ListView):
    model = Actor
    template_name = "catalog/actor_list.html"
    context_object_name = "actor_list"
    paginate_by = 6

    def get_queryset(self):
        queryset = Actor.objects.annotate(
            movie_count=Count("roles__movie", distinct=True)
        ).order_by("first_name", "last_name")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ActorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Actor
    template_name = "catalog/actor_detail.html"
    context_object_name = "actor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = self.object.roles.select_related("movie")
        return context

#class for MOVIE
class MovieListView(LoginRequiredMixin, generic.ListView):
    model = Movie
    template_name = "catalog/movie_list.html"
    context_object_name = "movie_list"
    ordering = ["-release_date"]
    paginate_by = 6

    def get_queryset(self):
        queryset = Movie.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class MovieDetailView(LoginRequiredMixin, generic.DetailView):
    model = Movie
    template_name = "catalog/movie_detail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = self.object.roles.select_related("actor")
        return context


@login_required
def toggle_director(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    user = request.user

    if user in movie.directors.all():
        movie.directors.remove(user)
    else:
        movie.directors.add(user)

    return redirect("catalog:movie_detail", pk=pk)


class RegisterDirectorView(generic.FormView):
    template_name = "registration/register_director.html"
    form_class = DirectorSignUpForm
    success_url = reverse_lazy("catalog:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class MovieCreateView(LoginRequiredMixin, generic.CreateView):
    model = Movie
    form_class = MovieCreateForm
    template_name = "catalog/create_movie.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.license_card:
            return render(request, "catalog/no_license.html")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = RoleInlineFormSet(self.request.POST)
        else:
            context["formset"] = RoleInlineFormSet()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.directors.add(self.request.user)

        formset = RoleInlineFormSet(self.request.POST)
        if formset.is_valid():
            roles = formset.save(commit=False)
            for role in roles:
                role.movie = self.object
                role.save()
        return response

    def get_success_url(self):
        return reverse("catalog:movie_detail", kwargs={"pk": self.object.pk})


def no_license_view(request):
    return render(request, "catalog/no_license.html")

