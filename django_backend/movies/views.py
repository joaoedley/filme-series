# movies/views.py
from rest_framework import viewsets, permissions
from .models import Category, Movie
from .serializers import CategorySerializer, MovieSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("-created_at")
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]