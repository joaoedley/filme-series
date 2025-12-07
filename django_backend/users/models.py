from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Campos extras no futuro (ex: plano, avatar etc.)
    favorites = models.ManyToManyField("movies.Movie", blank=True, related_name="fav_by_users")
    favorites_series = models.ManyToManyField("series.Series", blank=True, related_name="fav_by_users")