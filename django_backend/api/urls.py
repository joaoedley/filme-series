from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movies.views import CategoryViewSet, MovieViewSet
from series.views import SeriesViewSet, EpisodeViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"movies", MovieViewSet)
router.register(r"series", SeriesViewSet)
router.register(r"episodes", EpisodeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Aliases para o Node Admin (espera /auth/token/)
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair_alias"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh_alias"),

]