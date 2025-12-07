from django.urls import path
from .views import series_list, series_detail

app_name = "series"

urlpatterns = [
    path("", series_list, name="list"),
    path("<int:pk>/", series_detail, name="detail"),
]