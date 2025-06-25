import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from catalog.models import Movie, Actor, Role, Genre


class DirectorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    license_card = forms.CharField(max_length=100, required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2", "first_name", "last_name", "email", "license_card"]

    def clean_license_card(self):
        license_card = self.cleaned_data["license_card"]

        if not re.match(r"^[A-Z]{2}\d{6}$", license_card):
            raise ValidationError("The license format should be: 'AA123456' — 2: uppercase letters and 6: digits.")

        User = get_user_model()
        if User.objects.filter(license_card=license_card).exists():
            raise ValidationError("This license number is already in use.")

        return license_card


class DirectorUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "license_card"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "license_card": forms.TextInput(attrs={"class": "form-control"}),
        }


class MovieCreateForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "description", "release_date", "rating", "genres"]
        widgets = {
            "genres": forms.CheckboxSelectMultiple()
        }


RoleInlineFormSet = inlineformset_factory(
    Movie,
    Role,
    fields=["character_name", "actor"],
    extra=4,
    can_delete=True
)


class ActorCreateForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ["first_name", "last_name"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class GenreCreateForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }




