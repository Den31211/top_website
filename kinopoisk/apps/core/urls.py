from django.urls import path
from .views import APIRootView, HealthView, StatsView

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('health/', HealthView.as_view(), name='health'),
    path('stats/', StatsView.as_view(), name='stats'),
]
