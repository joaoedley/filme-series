from django.db import models
from movies.models import Category

class Series(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="series")
    cover_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Episode(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="episodes")
    title = models.CharField(max_length=200)
    season = models.PositiveIntegerField(default=1)
    number = models.PositiveIntegerField()
    video_path = models.CharField(max_length=255, blank=True)  # Bunny Storage path
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("series", "season", "number")
        ordering = ["season", "number"]

    def __str__(self):
        return f"{self.series.title} - T{self.season} Ep {self.number}: {self.title}"