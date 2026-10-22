from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet, ReviewViewSet

router = DefaultRouter()
router.register('ratings', RatingViewSet, basename='rating')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]