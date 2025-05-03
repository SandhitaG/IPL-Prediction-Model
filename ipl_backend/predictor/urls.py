from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, PlayerViewSet, MatchViewSet, PredictionViewSet

router = DefaultRouter()
router.register('teams', TeamViewSet)
router.register('players', PlayerViewSet)
router.register('matches', MatchViewSet)
router.register('predictions', PredictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
