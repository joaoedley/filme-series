# series/views.py
from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from movies.views import IsAdminOrReadOnly
from .models import Series, Episode
from .serializers import SeriesSerializer, EpisodeSerializer


# API ViewSets (mantidos)
class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAdminOrReadOnly]


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.select_related("series").all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAdminOrReadOnly]


# Helpers
def _is_abs(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def _full_video_url(bunny_host: str, path: str) -> str:
    if not path:
        return ""
    if _is_abs(path):
        return path
    host = bunny_host.rstrip("/") if bunny_host else ""
    pref = "/" if not path.startswith("/") else ""
    return f"https://{host}{pref}{path}" if host else path


# HTML Views
def series_list(request):
    items = Series.objects.order_by("-id")
    return render(request, "series_list.html", {"series": items})


def series_detail(request, pk: int):
    import os
    serie = get_object_or_404(Series.objects.prefetch_related("episodes"), pk=pk)
    eps = list(serie.episodes.order_by("season", "number"))

    bunny_host = os.getenv("BUNNY_CDN_PULL_ZONE_HOSTNAME", "")
    # inicial: primeiro da lista ordenada
    initial_video_url = _full_video_url(bunny_host, eps[0].video_path) if eps else ""

    # Constrói lista com URLs completas e inclui season
    episodes_ctx = [
        {
            "season": e.season,
            "number": e.number,
            "title": e.title,
            "video_url": _full_video_url(bunny_host, e.video_path),
        }
        for e in eps
    ]

    # Agrupa por temporada para o template
    seasons = []
    current = None
    for ep in episodes_ctx:
        if not current or current["season"] != ep["season"]:
            current = {"season": ep["season"], "episodes": []}
            seasons.append(current)
        current["episodes"].append(ep)

    return render(request, "series_detail.html", {
        "series": serie,
        "seasons": seasons,
        "episodes": episodes_ctx,  # restore list used by template
        "initial_video_url": initial_video_url,
    })