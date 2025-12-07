# series/serializers.py
from rest_framework import serializers
from .models import Series, Episode
from movies.serializers import CategorySerializer
from movies.models import Category

class SeriesSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True
    )
    class Meta:
        model = Series
        fields = ["id","title","description","year","category","category_id","cover_url","trailer_url"]

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id","series","title","number","video_path","created_at"]