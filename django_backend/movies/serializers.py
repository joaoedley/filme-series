# movies/serializers.py
from rest_framework import serializers
from .models import Category, Movie

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True
    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "year",
            "category",
            "category_id",
            "cover_url",
            "trailer_url",
            "video_path",
            "created_at",
        ]