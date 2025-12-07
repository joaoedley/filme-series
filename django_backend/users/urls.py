# users/urls.py
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.auth_login, name="login"),
    path("register/", views.auth_register, name="register"),
    path("favorites/", views.favorites_page, name="favorites"),
    path("favorite/movie/<int:movie_id>/", views.toggle_favorite_movie, name="fav_movie"),
    path("favorite/series/<int:series_id>/", views.toggle_favorite_series, name="fav_series"),
    path("jwt/", views.jwt_obtain_pair, name="jwt_obtain_pair"),
]