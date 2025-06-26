# MovieCore


Кінобаза для справжніх режисерів!  
MovieCore — це Django-застосунок для створення, перегляду та адміністрування фільмів, акторів, жанрів і режисерів із автентифікацією та гнучкими ролями.

---

![moviecore.png](static/screenshot/moviecore.png)


---
git clone https://github.com/your-username/moviecore.git
cd moviecore

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# (Optional) Load demo data
python manage.py loaddata movie_core_db_data.json

# Create superuser (for admin access)
python manage.py createsuperuser

# Or use:
#   admin.user  
#   1qazcde3

# Run server
python manage.py runserver


# Directors
Register at: /register/

License format is mandatory: AA123456 (2 uppercase letters + 6 digits)

Film creation is restricted to licensed users

Login / Logout: /login/ and /logout/



# Site Features
Movies: create, edit, delete, manage actor roles via FormSet, assign genres

Actors: detail pages, search, delete

Genres: movie counter, creation, search, delete

Directors: list, profiles, search, self-edit

Roles: characters, link actors to movies

Homepage: stats + top 3 movies

Access control: all pages require login


# Search Functionality
Available on pages: movies/, actors/, genres/, directors/


# Tests
python manage.py test

Tests cover:

Registration form validation (license_card)

Search within list views

Detail view navigation

Login, registration, logout pages


