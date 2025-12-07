from django.contrib import admin
from django.urls import path, include
from .views import home, search_view
from users.views import favorites_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("favorites/", favorites_page, name="favorites"),
    path("search/", search_view, name="search"),
    path("users/", include("users.urls")),
    path("movies/", include("movies.urls")),
    path("series/", include("series.urls")),
    path("api/", include("api.urls")),
]