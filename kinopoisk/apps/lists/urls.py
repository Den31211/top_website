from rest_framework.routers import DefaultRouter
from .views import MovieListViewSet, MovieListItemViewSet

router = DefaultRouter()
router.register('items', MovieListItemViewSet, basename='list-item')
router.register('', MovieListViewSet, basename='list')

urlpatterns = router.urls
