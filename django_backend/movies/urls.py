# movies/urls.py
from django.urls import path
from django.shortcuts import render, get_object_or_404
from .models import Movie
import os


def movies_list(request):
    items = Movie.objects.order_by("-created_at")
    return render(request, "movies_list.html", {"movies": items})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    host = os.getenv("BUNNY_CDN_PULL_ZONE_HOSTNAME", "").rstrip("/")
    path = movie.video_path or ""
    if path and not (path.startswith("http://") or path.startswith("https://")):
        if not path.startswith("/"):
            path = "/" + path
        initial_video_url = f"https://{host}{path}" if host else path
    else:
        initial_video_url = path
    return render(request, "movie_detail.html", {"movie": movie, "initial_video_url": initial_video_url})


urlpatterns = [
    path("", movies_list, name="movies_list"),
    path("<int:pk>/", movie_detail, name="movie_detail"),
]