from django.shortcuts import render
from movies.models import Movie, HomeBanner
from series.models import Series
from django.db.models import Q


def home(request):
    # cards das grades individuais
    movies = Movie.objects.order_by("-created_at")[:12]
    series = Series.objects.order_by("-id")[:12]

    # banners: 1) usa banners do Admin (HomeBanner); 2) se não houver, usa fallback de filmes/séries
    banners = []
    admin_banners = list(HomeBanner.objects.filter(is_active=True).order_by("position", "-created_at")[:10])
    if admin_banners:
        for b in admin_banners:
            banners.append({
                "title": b.title,
                "image": b.image_url,
                "trailer": b.trailer_url or "",
                "href": b.href or "#",
            })
    else:
        for m in Movie.objects.exclude(cover_url="").order_by("-created_at")[:6]:
            banners.append({
                "title": m.title,
                "image": m.cover_url,
                "trailer": m.trailer_url or "",
                "href": f"/movies/{m.id}/",
            })
        for s in Series.objects.exclude(cover_url="").order_by("-id")[:6]:
            banners.append({
                "title": s.title,
                "image": s.cover_url,
                "trailer": s.trailer_url or "",
                "href": f"/series/{s.id}/",
            })

    # Recentes: mistura últimos filmes e séries e ordena por chave de tempo (created_at para filmes, id para séries)
    recents = []
    for m in Movie.objects.order_by("-created_at")[:24]:
        recents.append({
            "kind": "movie",
            "sort_key": m.created_at.timestamp() if m.created_at else 0,
            "href": f"/movies/{m.id}/",
            "title": m.title,
            "year": m.year,
            "cover_url": m.cover_url,
        })
    for s in Series.objects.order_by("-id")[:24]:
        # usa id como proxy de recência
        recents.append({
            "kind": "series",
            "sort_key": float(s.id or 0),
            "href": f"/series/{s.id}/",
            "title": s.title,
            "year": s.year,
            "cover_url": s.cover_url,
        })
    recents = sorted(recents, key=lambda x: x["sort_key"], reverse=True)[:12]

    return render(request, "home.html", {
        "movies": movies,
        "series": series,
        "recents": recents,
        "banners": banners,
    })


def search_view(request):
    q = request.GET.get("q", "").strip()
    movies = []
    series = []
    if q:
        movies = Movie.objects.filter(Q(title__icontains=q) | Q(description__icontains=q)).order_by("-created_at")[:24]
        series = Series.objects.filter(Q(title__icontains=q) | Q(description__icontains=q)).order_by("-id")[:24]
    return render(request, "search.html", {"q": q, "movies": movies, "series": series})
