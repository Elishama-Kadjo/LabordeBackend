from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore
from rest_framework.routers import SimpleRouter  # type: ignore
from .views import (
    ContactPropertyAPIView,
    RealEstateViewSet,
    RealEstateFavoriteViewSet,
    CheckFavoriteExistenceView,
    RealEstateLikedViewSet,
)

router = SimpleRouter()

router.register("getrealestate", RealEstateViewSet, basename="real_estate")
router.register(
    "getrealestatefavorites", RealEstateLikedViewSet, basename="real_estate_favorite"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "single/realestate/<slug:real_estate>/favorite/",
        CheckFavoriteExistenceView.as_view(),
        name="check_favorite_existence",
    ),
    path(
        "realestate/getfavorites/",
        RealEstateFavoriteViewSet.as_view(),
        name="favorites",
    ),
    path('contact_property/', ContactPropertyAPIView.as_view(), name='contact_property'),

]
