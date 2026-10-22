from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet, CountryViewSet

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genre')
router.register('countries', CountryViewSet, basename='country')
router.register('', MovieViewSet, basename='movie')

urlpatterns = router.urls
