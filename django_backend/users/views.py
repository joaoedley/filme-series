# users/views.py
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

User = get_user_model()


def auth_login(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            messages.success(request, "Bem-vindo!")
            return redirect("home")
        messages.error(request, "Credenciais inválidas")
    return render(request, "auth_login.html")


def auth_register(request):
    if request.method == "POST":
        u = request.POST.get("username")
        e = request.POST.get("email")
        p = request.POST.get("password")
        if User.objects.filter(username=u).exists():
            messages.error(request, "Usuário já existe")
        else:
            user = User.objects.create_user(username=u, email=e, password=p)
            messages.success(request, "Conta criada! Faça login.")
            return redirect("users:login")
    return render(request, "auth_register.html")


@login_required
def favorites_page(request):
    movies = request.user.favorites.all()
    series = request.user.favorites_series.all()
    return render(request, "favorites.html", {"movies": movies, "series": series})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite_movie(request, movie_id):
    user = request.user
    from movies.models import Movie
    try:
        movie = Movie.objects.get(id=movie_id)
        if movie in user.favorites.all():
            user.favorites.remove(movie)
            fav = False
        else:
            user.favorites.add(movie)
            fav = True
        return JsonResponse({"favorite": fav})
    except Movie.DoesNotExist:
        return JsonResponse({"detail": "Not found"}, status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite_series(request, series_id):
    user = request.user
    from series.models import Series as SeriesModel
    try:
        s = SeriesModel.objects.get(id=series_id)
        if s in user.favorites_series.all():
            user.favorites_series.remove(s)
            fav = False
        else:
            user.favorites_series.add(s)
            fav = True
        return JsonResponse({"favorite": fav})
    except SeriesModel.DoesNotExist:
        return JsonResponse({"detail": "Not found"}, status=404)


@api_view(["POST"])
def jwt_obtain_pair(request):
    # Para Node Admin obter token
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if not user or not user.is_staff:
        return JsonResponse({"detail": "Invalid credentials or not admin"}, status=401)
    refresh = RefreshToken.for_user(user)
    return JsonResponse({"access": str(refresh.access_token), "refresh": str(refresh)})