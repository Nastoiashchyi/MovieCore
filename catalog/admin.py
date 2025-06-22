from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Director, Actor, Genre, Movie, Role

# 🔐 Адмінка для Director
@admin.register(Director)
class DirectorAdmin(UserAdmin):
    list_display = UserAdmin.list_display
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("first_name", "last_name", "email",)}),
    )

# 🎭 Актори
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name",)

# 🏷️ Жанри
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

# 🎬 Фільми
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "rating", "director")
    list_filter = ("genres", "release_date", "director")
    search_fields = ("title", "description")
    filter_horizontal = ("genres",)
    autocomplete_fields = ["director"]
    date_hierarchy = "release_date"

# 👥 Ролі
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("movie", "actor", "character_name")
    search_fields = ("character_name", "actor__first_name", "movie__title")
    list_filter = ("movie", "actor")
    autocomplete_fields = ["movie", "actor"]