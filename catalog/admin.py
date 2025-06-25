from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Director, Actor, Genre, Movie, Role


@admin.register(Director)
class DirectorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("license_card", )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("first_name", "last_name", "email", "username", "license_card")
    ordering = ("first_name",)
    fieldsets = UserAdmin.fieldsets + (
        ("Personal info", {"fields": ("license_card",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("first_name", "last_name", "email", "license_card")}),
    )


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")
    ordering = ("first_name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "rating", )
    list_filter = ("genres", "release_date", "directors")
    search_fields = ("title", "description")
    filter_horizontal = ("genres",)
    autocomplete_fields = ["directors"]
    date_hierarchy = "release_date"


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("character_name", "actor", "movie")
    search_fields = ("character_name", "actor__first_name", "movie__title")
    list_filter = ("movie", "actor")
    autocomplete_fields = ["movie", "actor"]
    ordering = ("movie__title",)