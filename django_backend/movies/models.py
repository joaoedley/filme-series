from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="movies")
    cover_url = models.URLField(blank=True)  # Cloudinary URL
    trailer_url = models.URLField(blank=True)  # YouTube link
    video_path = models.CharField(max_length=255, blank=True)  # caminho no Bunny Storage (ex: /movies/slug/file.m3u8)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "filme"
            candidate = base
            i = 1
            while Movie.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                i += 1
                candidate = f"{base}-{i}"
            self.slug = candidate
        super().save(*args, **kwargs)


class HomeBanner(models.Model):
    """Banners da página inicial, gerenciados pelo Admin."""
    title = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(help_text="URL da imagem/capa exibida no banner")
    trailer_url = models.URLField(blank=True, help_text="(Opcional) link do trailer")
    href = models.CharField(max_length=255, blank=True, help_text="(Opcional) link ao clicar. Ex: /movies/1/")
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0, help_text="Ordem de exibição (menor primeiro)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "-created_at"]

    def __str__(self):
        return f"{self.title} (ativo={self.is_active})"